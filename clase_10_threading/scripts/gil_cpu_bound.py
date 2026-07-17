#!/usr/bin/env python3
"""
gil_cpu_bound.py - Ejercicio 3 de Threading.

Demuestra que threads NO escalan para tareas CPU-bound (por el GIL).
La versión con 4 threads tarda lo mismo o más que la secuencial.

Probalo reemplazando threading por multiprocessing.Process para ver
el speedup real con CPU-bound.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import math
import threading
import time


def cpu_task(n):
    return sum(math.sqrt(i) for i in range(n))


def main():
    N = 5_000_000

    # Secuencial
    inicio = time.perf_counter()
    for _ in range(4):
        cpu_task(N)
    print(f"Secuencial:  {time.perf_counter() - inicio:.2f}s")

    # Con 4 threads
    inicio = time.perf_counter()
    hilos = [threading.Thread(target=cpu_task, args=(N,)) for _ in range(4)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    print(f"4 threads:   {time.perf_counter() - inicio:.2f}s")


if __name__ == "__main__":
    main()
