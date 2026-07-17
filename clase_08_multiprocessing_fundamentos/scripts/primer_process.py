#!/usr/bin/env python3
"""
primer_process.py - Ejercicio 1 de Multiprocessing fundamentos.

Crea un proceso con multiprocessing.Process. El proceso imprime
su PID y su padre, duerme 2 segundos y termina.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import os
import time
from multiprocessing import Process


def tarea(nombre):
    print(f"[{nombre}] PID={os.getpid()}, parent={os.getppid()}", flush=True)
    time.sleep(2)
    print(f"[{nombre}] termino", flush=True)


def main():
    p = Process(target=tarea, args=("Worker",))
    p.start()
    p.join()
    print(f"[Main] PID={os.getpid()}, exitcode={p.exitcode}")


if __name__ == "__main__":
    main()
