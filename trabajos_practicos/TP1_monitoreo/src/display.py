"""
display.py — la TUI del monitor.

Usa rich (que ya está en requirements.txt). Estructura:

    ┌────────────────────────────┐
    │ Header: vista activa + info│
    ├────────────────────────────┤
    │ Lista de procesos          │  ← siempre visible
    ├────────────────────────────┤
    │ Panel de detalle (vista)   │  ← cambia según la vista activa
    └────────────────────────────┘

Vista activa: índice 0..6 (resumen, memoria, fds, threads, senales,
scheduling, sistema). Se cambia con teclas 1..7 o r/m/f/t/s/p/g.

El input de teclado es NO BLOQUEANTE: usamos un thread daemon que lee de
sys.stdin y pone las teclas en una queue local. El loop principal de
render consume esa queue.

¿Por qué thread y no select() directo?
    - select() sobre sys.stdin es un quilombo en Windows (no anda bien con fd 0
      y stdin de consola). Con un thread daemon, "anda en todos lados".
    - Es lo que hace la consigna: "podés usar threads internamente dentro
      del proceso de display para la entrada de teclado (no es obligatorio)".
"""

import os
import queue
import select
import sys
import threading
import time
from datetime import datetime

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .agregador import SLOTS, leer_slot
from .procfs import ESTADOS


# Nombres de las 7 vistas y teclas que las activan.
VISTAS = [
    ("1", "r", "Resumen"),
    ("2", "m", "Memoria"),
    ("3", "f", "File descriptors"),
    ("4", "t", "Threads"),
    ("5", "s", "Señales"),
    ("6", "p", "Scheduling"),
    ("7", "g", "Sistema global"),
]
NOMBRE_SLOT = ["resumen", "memoria", "fds", "threads", "senales", "scheduling", "sistema"]


def _teclado_thread(q_teclas):
    """Lee teclas de stdin en un thread daemon y las pone en la queue.

    Lee carácter por carácter. La lectura es bloqueante (en este thread),
    pero como el thread es daemon y separado, no bloquea el render.
    """
    try:
        fd = sys.stdin.fileno()
    except (ValueError, OSError):
        return
    while True:
        try:
            # Leemos 1 byte. Si estamos en tty, va línea por línea y se
            # comporta más o menos OK; si no, es modo cooked y se complica
            # para teclas como flechas. Para los básicos (1..7, q, /, c,
            # +/-, Enter) alcanza.
            data = os.read(fd, 1)
            if not data:
                break
            q_teclas.put(data.decode("utf-8", errors="replace"))
        except (OSError, ValueError):
            # Si el read falla (tty cerrado, etc.) salimos silencioso.
            time.sleep(0.1)
            continue


def _procesar_tecla(tecla, estado):
    """Actualiza el estado de la TUI según la tecla recibida.

    estado es un dict con: vista, intervalo_idx, ordenado_por, filtro_cmd,
    pin, verbose, last_msg, last_msg_ts.
    """
    if tecla in ("1", "2", "3", "4", "5", "6", "7"):
        estado["vista"] = int(tecla) - 1
    elif tecla in ("r", "m", "f", "t", "s", "p", "g"):
        mapeo = {"r": 0, "m": 1, "f": 2, "t": 3, "s": 4, "p": 5, "g": 6}
        estado["vista"] = mapeo[tecla]
    elif tecla == "q":
        estado["salir"] = True
    elif tecla == "c":
        ordenes = ["cpu_pct", "vm_rss", "pid"]
        idx = ordenes.index(estado["ordenado_por"]) if estado["ordenado_por"] in ordenes else 0
        estado["ordenado_por"] = ordenes[(idx + 1) % len(ordenes)]
    elif tecla in ("+", "="):
        idx = estado["vista"]
        if "intervalos" in estado and NOMBRE_SLOT[idx] in estado["intervalos"]:
            actual = estado["intervalos"][NOMBRE_SLOT[idx]].value
            estado["intervalos"][NOMBRE_SLOT[idx]].value = max(0.1, actual * 0.7)
            estado["last_msg"] = f"intervalo {NOMBRE_SLOT[idx]} → {estado['intervalos'][NOMBRE_SLOT[idx]].value:.2f}s"
            estado["last_msg_ts"] = time.time()
    elif tecla == "-":
        idx = estado["vista"]
        if "intervalos" in estado and NOMBRE_SLOT[idx] in estado["intervalos"]:
            actual = estado["intervalos"][NOMBRE_SLOT[idx]].value
            estado["intervalos"][NOMBRE_SLOT[idx]].value = min(60.0, actual * 1.5)
            estado["last_msg"] = f"intervalo {NOMBRE_SLOT[idx]} → {estado['intervalos'][NOMBRE_SLOT[idx]].value:.2f}s"
            estado["last_msg_ts"] = time.time()


def _armar_lista_procesos(snapshot, estado):
    """Devuelve la tabla con la lista de procesos (la parte de arriba de la TUI)."""
    _, datos = leer_slot(snapshot, "resumen")
    _, mem = leer_slot(snapshot, "memoria")

    if not datos:
        return Panel(Text("Esperando primer ciclo del analizador de resumen...",
                          style="dim"), title="Procesos")

    # Filtrar y ordenar.
    procs = []
    for pid, info in datos.items():
        if estado["filtro_cmd"] and estado["filtro_cmd"] not in info.get("comando", ""):
            continue
        rss = mem.get(pid, {}).get("vm_rss", 0)
        cpu = info.get("cpu_pct", 0)
        procs.append({
            "pid": pid,
            "estado": info.get("estado", "?"),
            "comando": (info.get("comando", "") or "")[:50],
            "comm": info.get("comm", ""),
            "threads": info.get("threads", 0),
            "cpu": cpu,
            "rss": rss,
        })

    clave = estado["ordenado_por"]
    procs.sort(key=lambda p: p.get(clave, 0) if clave != "pid" else p["pid"],
               reverse=(clave != "pid"))

    tabla = Table(show_header=True, header_style="bold cyan", expand=True)
    tabla.add_column("PID", justify="right", style="cyan", no_wrap=True, width=6)
    tabla.add_column("S", width=1)
    tabla.add_column("CPU%", justify="right", width=6)
    tabla.add_column("RSS(MB)", justify="right", width=8)
    tabla.add_column("THR", justify="right", width=4)
    tabla.add_column("Comando", overflow="ellipsis")

    for p in procs[:30]:  # máximo 30 filas para que entre en pantalla
        tabla.add_row(
            str(p["pid"]),
            p["estado"],
            f"{p['cpu']:.1f}",
            f"{p['rss'] / 1024:.1f}",
            str(p["threads"]),
            p["comando"] or p["comm"],
        )

    titulo = f"Procesos ({len(procs)} total) — orden: {estado['ordenado_por']}"
    return Panel(tabla, title=titulo, border_style="cyan")


def _vista_detalle(snapshot, estado, verbose):
    """Devuelve el panel de detalle de la vista activa."""
    idx = estado["vista"]
    slot = NOMBRE_SLOT[idx]
    nombre = VISTAS[idx][2]
    ts, datos = leer_slot(snapshot, slot)
    intervalo = estado["intervalos"][slot].value if "intervalos" in estado else 0

    if not datos:
        cuerpo = Text(f"Esperando primer ciclo del analizador '{slot}'...", style="dim")
    elif slot == "resumen":
        cuerpo = _render_resumen(datos, verbose)
    elif slot == "memoria":
        cuerpo = _render_memoria(datos, verbose)
    elif slot == "fds":
        cuerpo = _render_fds(datos, verbose)
    elif slot == "threads":
        cuerpo = _render_threads(datos, verbose)
    elif slot == "senales":
        cuerpo = _render_senales(datos, verbose)
    elif slot == "scheduling":
        cuerpo = _render_scheduling(datos, verbose)
    elif slot == "sistema":
        cuerpo = _render_sistema(snapshot, verbose)
    else:
        cuerpo = Text(f"Vista '{slot}' pendiente de implementar", style="yellow")

    edad = time.time() - ts if ts else 0
    titulo = f"Vista {idx+1}/{len(VISTAS)}: {nombre}   [intervalo={intervalo:.1f}s, edad={edad:.1f}s]"
    return Panel(cuerpo, title=titulo, border_style="green")


def _render_resumen(datos, verbose):
    """Vista 1: tabla con PID, estado, comando, threads, CPU%."""
    tabla = Table(show_header=True, header_style="bold", expand=True)
    tabla.add_column("PID", justify="right", width=6)
    tabla.add_column("Estado", width=18)
    tabla.add_column("THR", justify="right", width=4)
    tabla.add_column("CPU%", justify="right", width=7)
    tabla.add_column("UID", width=6)
    tabla.add_column("Comando")
    for pid in sorted(datos.keys())[:25]:
        d = datos[pid]
        estado_txt = ESTADOS.get(d["estado"], d["estado"])
        tabla.add_row(
            str(pid),
            f"{d['estado']} {estado_txt}",
            str(d.get("threads", 0)),
            f"{d.get('cpu_pct', 0):.2f}",
            str(d.get("uid", "?")),
            (d.get("comando", "") or "")[:80],
        )
    return tabla


def _render_memoria(datos, verbose):
    tabla = Table(show_header=True, header_style="bold", expand=True)
    tabla.add_column("PID", justify="right", width=6)
    tabla.add_column("VmSize", justify="right", width=10)
    tabla.add_column("VmRSS", justify="right", width=10)
    tabla.add_column("VmData", justify="right", width=10)
    tabla.add_column("VmSwap", justify="right", width=10)
    tabla.add_column("MinFlt", justify="right", width=8)
    tabla.add_column("MajFlt", justify="right", width=8)
    for pid in sorted(datos.keys())[:25]:
        d = datos[pid]
        tabla.add_row(
            str(pid),
            f"{d.get('vm_size', 0) / 1024:.1f} MB",
            f"{d.get('vm_rss', 0) / 1024:.1f} MB",
            f"{d.get('vm_data', 0) / 1024:.1f} MB",
            f"{d.get('vm_swap', 0) / 1024:.1f} MB",
            str(d.get("minflt", 0)),
            str(d.get("majflt", 0)),
        )
    return tabla


def _render_fds(datos, verbose):
    tabla = Table(show_header=True, header_style="bold", expand=True)
    tabla.add_column("PID", justify="right", width=6)
    tabla.add_column("FDs", justify="right", width=5)
    tabla.add_column("Primeros destinos")
    for pid in sorted(datos.keys())[:25]:
        fds = datos[pid]
        destinos = ", ".join(f"{d['n']}→{d['destino'][:40]}" for d in fds[:5])
        if len(fds) > 5:
            destinos += f" ... (+{len(fds) - 5})"
        tabla.add_row(str(pid), str(len(fds)), destinos)
    return tabla


def _render_threads(datos, verbose):
    tabla = Table(show_header=True, header_style="bold", expand=True)
    tabla.add_column("PID", justify="right", width=6)
    tabla.add_column("TID", justify="right", width=6)
    tabla.add_column("Estado", width=3)
    tabla.add_column("Nombre")
    tabla.add_column("CPU%", justify="right", width=7)
    for pid in sorted(datos.keys())[:15]:
        for t in datos[pid][:5]:
            tabla.add_row(
                str(pid), str(t["tid"]), t["estado"],
                t.get("comm", "")[:30],
                f"{t.get('cpu_pct', 0):.2f}",
            )
    return tabla


def _render_senales(datos, verbose):
    tabla = Table(show_header=True, header_style="bold", expand=True)
    tabla.add_column("PID", justify="right", width=6)
    tabla.add_column("Bloqueadas", overflow="ellipsis")
    tabla.add_column("Ignoradas", overflow="ellipsis")
    tabla.add_column("Con handler", overflow="ellipsis")
    for pid in sorted(datos.keys())[:25]:
        d = datos[pid]
        tabla.add_row(
            str(pid),
            ", ".join(d.get("SigBlk_nombres", [])) or d.get("SigBlk", "?"),
            ", ".join(d.get("SigIgn_nombres", [])) or d.get("SigIgn", "?"),
            ", ".join(d.get("SigCgt_nombres", [])) or d.get("SigCgt", "?"),
        )
    return tabla


def _render_scheduling(datos, verbose):
    tabla = Table(show_header=True, header_style="bold", expand=True)
    tabla.add_column("PID", justify="right", width=6)
    tabla.add_column("Nice", justify="right", width=5)
    tabla.add_column("Prio", justify="right", width=5)
    tabla.add_column("RT", justify="right", width=4)
    tabla.add_column("Policy", width=24)
    tabla.add_column("CPUs", width=10)
    tabla.add_column("v_ctx/nv_ctx", width=15)
    for pid in sorted(datos.keys())[:25]:
        d = datos[pid]
        tabla.add_row(
            str(pid),
            str(d.get("nice", 0)),
            str(d.get("priority", 0)),
            str(d.get("rt_priority", 0)),
            d.get("policy_nombre", "?"),
            d.get("cpus_allowed", "?"),
            f"{d.get('voluntary_ctxt', 0)}/{d.get('nonvoluntary_ctxt', 0)}",
        )
    return tabla


def _render_sistema(snapshot, verbose):
    ts, datos = leer_slot(snapshot, "sistema")
    if not datos:
        return Text("Esperando primer ciclo de 'sistema'...", style="dim")

    texto = Text()
    texto.append(f"CPU global: {datos.get('cpu_pct', 0):.2f}%\n", style="bold cyan")
    texto.append(f"Procesos vistos: {datos.get('total_procesos', 0)}  ")
    texto.append(f"Threads: {datos.get('total_threads', 0)}  ")
    texto.append(f"Zombies: {datos.get('zombies', 0)}\n", style="red" if datos.get("zombies", 0) else "dim")
    texto.append(f"MemTotal: {datos.get('mem_total', 0) / 1024:.0f} MB  ")
    texto.append(f"MemFree: {datos.get('mem_free', 0) / 1024:.0f} MB  ")
    texto.append(f"MemAvailable: {datos.get('mem_available', 0) / 1024:.0f} MB\n")
    texto.append(f"Swap: {datos.get('swap_total', 0) / 1024:.0f}/{datos.get('swap_free', 0) / 1024:.0f} MB\n")
    la = datos.get("loadavg", {})
    texto.append(f"Load avg: {la.get('1min', 0):.2f} {la.get('5min', 0):.2f} {la.get('15min', 0):.2f}\n")
    estados = datos.get("conteo_estados", {})
    texto.append("Por estado: ")
    for est, cant in sorted(estados.items()):
        nombre = ESTADOS.get(est, est)
        texto.append(f"  {est}={cant} ({nombre})")
    texto.append("\n")

    top_cpu = datos.get("top_cpu", [])
    top_mem = datos.get("top_mem", [])
    if top_cpu:
        texto.append("\nTop CPU: " + ", ".join(str(x) for x in top_cpu) + "\n")
    if top_mem:
        texto.append("Top MEM: " + ", ".join(str(x) for x in top_mem) + "\n")

    return texto


def _armar_header(estado):
    ahora = datetime.now().strftime("%H:%M:%S")
    idx = estado["vista"]
    nombre = VISTAS[idx][2]
    help_ = "1-7: vista  c: orden  +-: intervalo  q: salir"
    if estado.get("last_msg") and (time.time() - estado.get("last_msg_ts", 0)) < 3:
        help_ = estado["last_msg"] + "  |  " + help_
    return Panel(
        Text(f"Monitor TP1 — {ahora}  |  Vista {idx+1}: {nombre}  |  {help_}",
             style="bold white on blue"),
        height=3,
    )


def display_loop(snapshot, intervalos, verbose_flag, stop_event=None):
    """Loop principal del display. Corre hasta que se setee stop_event o el usuario presione 'q'."""
    console = Console()
    estado = {
        "vista": 0,
        "ordenado_por": "cpu_pct",
        "filtro_cmd": "",
        "pin": None,
        "salir": False,
        "intervalos": intervalos,
        "verbose": verbose_flag,
        "last_msg": "",
        "last_msg_ts": 0,
    }

    # Thread daemon para el teclado.
    q_teclas = queue.Queue()
    t = threading.Thread(target=_teclado_thread, args=(q_teclas,), daemon=True)
    t.start()

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="procs", size=18),
        Layout(name="detalle"),
    )

    try:
        with Live(layout, console=console, refresh_per_second=4, screen=True) as live:
            while not estado["salir"]:
                # Drenar teclas pendientes.
                while True:
                    try:
                        tecla = q_teclas.get_nowait()
                    except queue.Empty:
                        break
                    _procesar_tecla(tecla, estado)

                verbose = verbose_flag.value if hasattr(verbose_flag, "value") else False
                layout["header"].update(_armar_header(estado))
                layout["procs"].update(_armar_lista_procesos(snapshot, estado))
                layout["detalle"].update(_vista_detalle(snapshot, estado, verbose))

                time.sleep(0.25)  # 4 fps de redibujo
    except KeyboardInterrupt:
        pass

    if stop_event is not None:
        stop_event.set()


if __name__ == "__main__":
    # Mini-prueba: sin multiprocessing, con un snapshot fake.
    snap_fake = {
        "resumen": {
            "ts": time.time(),
            "datos": {
                1: {"pid": 1, "estado": "S", "comm": "systemd", "comando": "/sbin/init",
                    "threads": 1, "cpu_pct": 0.1, "uid": "0"},
                100: {"pid": 100, "estado": "R", "comm": "python3", "comando": "python3 monitor.py",
                      "threads": 4, "cpu_pct": 12.5, "uid": "1000"},
            },
        },
        "memoria": {
            "ts": time.time(),
            "datos": {
                1: {"vm_size": 100000, "vm_rss": 5000, "vm_data": 100, "vm_swap": 0, "minflt": 100, "majflt": 0},
                100: {"vm_size": 80000, "vm_rss": 30000, "vm_data": 5000, "vm_swap": 0, "minflt": 500, "majflt": 2},
            },
        },
        "sistema": {
            "ts": time.time(),
            "datos": {
                "cpu_pct": 15.2, "mem_total": 8 * 1024 * 1024, "mem_free": 4 * 1024 * 1024,
                "mem_available": 5 * 1024 * 1024, "swap_total": 0, "swap_free": 0,
                "loadavg": {"1min": 0.5, "5min": 0.4, "15min": 0.3},
                "total_procesos": 2, "total_threads": 5, "zombies": 0,
                "conteo_estados": {"S": 1, "R": 1},
                "top_cpu": [], "top_mem": [],
            },
        },
    }
    # Para probar de verdad hay que tener un Manager; este test solo verifica
    # que el módulo importa sin errores.
    print("display.py importa OK. Para ver la TUI correr docker compose up.")
