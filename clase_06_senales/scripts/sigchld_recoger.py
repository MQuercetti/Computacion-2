#!/usr/bin/env python3
"""
sigchld_recoger.py - Ejercicio 3.2 de Señales.

Usa SIGCHLD para detectar cuándo terminan los hijos sin bloquear.
El handler hace waitpid(-1, WNOHANG) en un loop para recoger todos
los hijos que hayan terminado.

Prerequisito: solo Linux/macOS.
"""
import os
import signal
import time

hijos_activos = set()
resultados = {}


def sigchld_handler(sig, frame):
    """Recoger hijos terminados sin bloquear."""
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
            hijos_activos.discard(pid)
            codigo = os.WEXITSTATUS(status) if os.WIFEXITED(status) else -1
            resultados[pid] = codigo
            print(f"[SIGCHLD] Hijo {pid} terminó con código {codigo}", flush=True)
        except ChildProcessError:
            break


def main():
    signal.signal(signal.SIGCHLD, sigchld_handler)

    print("Creando 5 hijos...", flush=True)
    for i in range(5):
        pid = os.fork()
        if pid == 0:
            duracion = (i + 1) * 0.5
            time.sleep(duracion)
            os._exit(i)
        else:
            hijos_activos.add(pid)
            print(f"Creado hijo {pid}, durará {(i+1)*0.5}s", flush=True)

    print("\n[PADRE] Trabajando mientras los hijos se ejecutan...", flush=True)
    for tick in range(10):
        print(f"[PADRE] Tick {tick}, hijos activos: {len(hijos_activos)}", flush=True)
        time.sleep(0.5)
        if not hijos_activos:
            break

    print(f"\n[PADRE] Todos terminaron. Resultados: {resultados}", flush=True)


if __name__ == "__main__":
    main()
