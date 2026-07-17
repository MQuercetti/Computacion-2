"""
senales.py — manejo async-signal-safe de las 5 señales del monitor.

Patrón self-pipe (visto en clase 6: servidor_signals.py, shutdown_limpio.py):

    1. Creamos un par de sockets/pipe.
    2. El HANDLER de cada señal SOLO escribe un byte al extremo de escritura.
       Eso es async-signal-safe (write() está en la lista de syscalls seguras).
    3. El LOOP PRINCIPAL hace select() sobre el extremo de lectura y procesa
       la señal en contexto normal (puede imprimir, lockear, mandar mensajes
       a queues, etc.).

¿Por qué no hacemos el trabajo adentro del handler?
    - printf, malloc, logging, lock(), etc. NO son async-signal-safe.
    - Si los llamás desde el handler, podés deadlockear o corromper memoria.
    - La consigna lo dice explícitamente: "Todos los handlers deben ser
      async-signal-safe. Usar el patrón self-pipe o signal.set_wakeup_fd".

Señales que manejamos (la consigna pide estas 5):
    SIGINT   → shutdown limpio
    SIGTERM  → shutdown limpio
    SIGHUP   → recargar config
    SIGUSR1  → dump del snapshot a JSON
    SIGUSR2  → toggle verbose

SIGWINCH (terminal redimensionada) la dejamos opcional más adelante.
"""

import errno
import json
import os
import signal
import time
from datetime import datetime


def crear_self_pipe():
    """Crea un par de pipe() para el self-pipe pattern.

    Devuelve (r_fd, w_fd). El handler va a escribir a w_fd; el loop principal
    lee de r_fd.

    Usamos os.pipe() y no multiprocessing.Pipe porque los fd son más livianos
    y los podemos pasar a signal.set_wakeup_fd si hace falta.
    """
    r, w = os.pipe()
    return r, w


def instalar_manejadores(write_fd, pid_display=None):
    """Instala los 5 handlers de señales.

    Cada handler es mínimo: solo escribe el número de señal (1 byte) a write_fd.
    El loop principal lo lee y procesa.

    Si pid_display se pasa, SIGUSR1 se manda al display (para que él haga el
    dump). Si no, lo hace el proceso principal.
    """
    # Capturamos qué señal llegó usando signal.Signals (un valor distinto
    # por handler). Pero write() solo escribe 1 byte, así que codificamos
    # el número de señal como 1 byte (señales 1..255 caben).
    def _handler(signum, frame):
        try:
            os.write(write_fd, bytes([signum & 0xFF]))
        except OSError:
            pass  # pipe cerrado, estamos cerrando

    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)
    signal.signal(signal.SIGHUP, _handler)
    signal.signal(signal.SIGUSR1, _handler)
    signal.signal(signal.SIGUSR2, _handler)


def leer_signal_no_bloqueante(read_fd):
    """Lee 1 byte del pipe sin bloquear. Devuelve la señal (int) o None si no hay nada."""
    try:
        data = os.read(read_fd, 1)
    except OSError as e:
        if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
            return None
        raise
    if not data:
        return None
    return data[0]


def procesar_evento(signum, snapshot, intervalos, config_path, verbose_flag):
    """Procesa una señal recibida. Se llama desde el loop principal, NO desde el handler.

    Devuelve un string indicando la acción tomada (para que main.py pueda
    loguear o decidir si apagar el monitor).
    """
    if signum == signal.SIGINT or signum == signal.SIGTERM:
        return "shutdown"

    if signum == signal.SIGHUP:
        try:
            with open(config_path, "r") as f:
                cfg = json.load(f)
            for slot, valor in cfg.items():
                if slot in intervalos:
                    intervalos[slot].value = float(valor)
            return f"reload_ok: {cfg}"
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            return f"reload_error: {e}"

    if signum == signal.SIGUSR1:
        return _dump_snapshot(snapshot)

    if signum == signal.SIGUSR2:
        verbose_flag.value = not verbose_flag.value
        estado = "ON" if verbose_flag.value else "OFF"
        return f"verbose_toggle: {estado}"

    return f"senal_desconocida: {signum}"


def _dump_snapshot(snapshot):
    """Escribe el snapshot a /app/dumps/dump_<timestamp>.json."""
    # Directorio de dumps: dentro del WORKDIR del container (/app).
    dumps_dir = os.path.join(os.getcwd(), "dumps")
    os.makedirs(dumps_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = os.path.join(dumps_dir, f"dump_{ts}.json")

    # Convertimos el snapshot (que tiene Manager.dict por dentro) a un dict
    # serializable normal.
    serializable = {}
    for slot, contenido in snapshot.items():
        # contenido es un dict con 'ts' y 'datos'
        serializable[slot] = {
            "ts": contenido.get("ts", 0),
            "datos": _a_serializable(contenido.get("datos", {})),
        }

    with open(ruta, "w") as f:
        json.dump(serializable, f, indent=2, default=str)
    return f"dump_ok: {ruta}"


def _a_serializable(obj):
    """Convierte recursivamente lo que haya en el snapshot a tipos JSON-amigables."""
    if isinstance(obj, dict):
        return {str(k): _a_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_a_serializable(x) for x in obj]
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    return str(obj)


# TODO: ¿cómo manejarías SIGWINCH (terminal redimensionada) si el display
# necesita repintarse? Pista: la señal ya llega; lo que hay que decidir es
# QUÉ proceso la procesa. Si el handler está en main.py y la TUI está en
# otro proceso, ¿cómo le avisás al display que redibuje? (mirar el patrón
# de multiprocessing.Event o un Queue dedicado para el display).
