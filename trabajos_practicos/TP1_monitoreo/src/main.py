"""
main.py — entry point del monitor de procesos.

Flujo:
    1. Cargar config.json (intervalos por defecto).
    2. Crear IPC:
        - Manager().dict()    → snapshot global compartido entre los 7 analizadores y el display.
        - Manager().dict()    → intervalos por vista (Value('d') cada uno, ajustables con + / -).
        - multiprocessing.Value('b') → flag de verbose (toggle con SIGUSR2).
        - multiprocessing.Queue       → PIDs que el recolector publica.
        - multiprocessing.Event       → stop_event para shutdown cooperativo.
    3. Instalar handlers de señales con self-pipe.
    4. Lanzar procesos:
        - 1 Recolector (1s).
        - 7 Analizadores (cada uno con su intervalo). Todos daemon=True.
        - 1 Display (no-daemon, es el front-end).
    5. Loop principal: select() sobre el self-pipe, procesa señales.
    6. Cuando llega SIGINT/SIGTERM: stop_event.set(), join hijos, salir.
"""

import errno
import json
import multiprocessing as mp
import os
import select
import signal
import sys
import time
import traceback

from . import display, procfs, senales
from .agregador import (
    SLOTS,
    crear_intervalos,
    crear_lock_global,
    crear_snapshot,
)
from .analizadores import fds, memoria, resumen, scheduling, senales as an_senales, sistema, threads
from .recolector import recolector_loop


CONFIG_PATH = os.environ.get("MONITOR_CONFIG", "/app/config.json")


def _cargar_config():
    """Carga config.json o usa defaults si no existe."""
    defaults = {s: 2.0 for s in SLOTS}
    defaults["fds"] = 5.0
    defaults["senales"] = 10.0
    defaults["scheduling"] = 10.0
    try:
        with open(CONFIG_PATH, "r") as f:
            return {**defaults, **json.load(f)}
    except (FileNotFoundError, json.JSONDecodeError):
        return defaults


def _lanzar_analizador(target, q_pids, snapshot, intervalos, lock, verbose, name):
    """Helper: crea y arranca un Process con los args comunes."""
    p = mp.Process(
        target=_wrapper_analizador,
        args=(target, q_pids, snapshot, intervalos, lock, verbose),
        name=name,
        daemon=True,
    )
    p.start()
    return p


def _wrapper_analizador(target, q_pids, snapshot, intervalos, lock, verbose):
    """Wrapper que espera el primer lote de PIDs y llama al loop del analizador.

    Si el analizador crashea, lo logueamos y salimos del proceso (no tiramos
    abajo todo el monitor).
    """
    try:
        # Primer lote (bloqueante).
        pids = q_pids.get()
        while True:
            # Si el recolector publicó un lote más reciente, lo usamos.
            while not q_pids.empty():
                pids = q_pids.get_nowait()
            target(pids, snapshot, intervalos, verbose)
            # Si llegamos acá, target retornó (no debería, son loops infinitos).
            time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        return
    except Exception as e:
        print(f"[ERROR analizador {target.__name__}] {e}", file=sys.stderr)
        traceback.print_exc()


def main():
    cfg = _cargar_config()
    print(f"[main] config cargada: {cfg}")

    # 1. IPC.
    mgr_snap, snapshot = crear_snapshot()
    mgr_int, intervalos = crear_intervalos(cfg)
    lock = crear_lock_global()
    verbose = mgr_int.Value("b", False)  # flag global de verbose
    q_pids = mp.Queue(maxsize=2)         # últimos PIDs publicados
    stop_event = mp.Event()

    # 2. Señales con self-pipe.
    r_fd, w_fd = senales.crear_self_pipe()
    # Ponemos el fd de lectura en no-bloqueante para el select().
    os.set_blocking(r_fd, False)
    senales.instalar_manejadores(w_fd)

    # 3. Recolector.
    p_recolector = mp.Process(
        target=recolector_loop,
        args=(q_pids, 1.0),
        name="Recolector",
        daemon=True,
    )
    p_recolector.start()
    print(f"[main] Recolector PID={p_recolector.pid}")

    # 4. Analizadores.
    targets = [
        (resumen.analizar, "Resumen"),
        (memoria.analizar, "Memoria"),
        (fds.analizar, "FDs"),
        (threads.analizar, "Threads"),
        (an_senales.analizar, "Senales"),
        (scheduling.analizar, "Scheduling"),
        (sistema.analizar, "Sistema"),
    ]
    analizadores = []
    for target, nombre in targets:
        p = _lanzar_analizador(target, q_pids, snapshot, intervalos, lock, verbose, nombre)
        analizadores.append(p)
        print(f"[main] {nombre} PID={p.pid}")

    # 5. Display (no-daemon, es el proceso principal visible).
    p_display = mp.Process(
        target=display.display_loop,
        args=(snapshot, intervalos, verbose, stop_event),
        name="Display",
        daemon=False,
    )
    p_display.start()
    print(f"[main] Display PID={p_display.pid}")

    # 6. Loop de señales.
    print("[main] monitor corriendo. Ctrl+C para salir.")
    try:
        while not stop_event.is_set():
            # select() con timeout corto para no comerse la CPU.
            r, _, _ = select.select([r_fd], [], [], 0.5)
            if r_fd in r:
                signum = senales.leer_signal_no_bloqueante(r_fd)
                if signum is not None:
                    accion = senales.procesar_evento(
                        signum, snapshot, intervalos, CONFIG_PATH, verbose,
                    )
                    print(f"[main] señal={signum} → {accion}")
                    if accion == "shutdown":
                        stop_event.set()
                        break
            # Si el display muere, también cerramos.
            if not p_display.is_alive():
                print("[main] display terminó, saliendo")
                stop_event.set()
                break
    except KeyboardInterrupt:
        print("[main] Ctrl+C, iniciando shutdown")
        stop_event.set()

    # 7. Shutdown limpio.
    _shutdown(p_display, analizadores, p_recolector, w_fd, r_fd)


def _shutdown(p_display, analizadores, p_recolector, w_fd, r_fd):
    print("[main] shutdown: terminando hijos...")
    if p_display.is_alive():
        p_display.terminate()
        p_display.join(timeout=2)
    for p in analizadores:
        if p.is_alive():
            p.terminate()
            p.join(timeout=1)
    if p_recolector.is_alive():
        p_recolector.terminate()
        p_recolector.join(timeout=1)
    try:
        os.close(w_fd)
    except OSError:
        pass
    try:
        os.close(r_fd)
    except OSError:
        pass
    print("[main] monitor apagado.")


if __name__ == "__main__":
    # multiprocessing en Linux/macOS usa fork por defecto, en Windows usa spawn.
    # spawn es más seguro (no hereda estado raro) pero más lento al arrancar.
    # Para el TP, spawn está bien.
    mp.set_start_method("spawn", force=True)
    main()
