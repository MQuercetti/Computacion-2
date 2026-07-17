#!/usr/bin/env python3
"""
speedup_cpu.py - Ejercicio 2 de Multiprocessing avanzado.

Mide speedup de multiprocessing.Pool con tareas CPU-bound.
Compara secuencial vs 1, 2, 4, 8 workers.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import math
import time
from multiprocessing import Pool


def cpu_task(n):
    """Tarea CPU-intensive: sumar raíces cuadradas."""
    return sum(math.sqrt(i) for i in range(n))


def main():
    N = 500_000
    TAREAS = 8

    # Secuencial
    inicio = time.time()
    resultados = [cpu_task(N) for _ in range(TAREAS)]
    t_seq = time.time() - inicio
    print(f"Secuencial:  {t_seq:.2f}s")

    for workers in [1, 2, 4, 8]:
        inicio = time.time()
        with Pool(workers) as pool:
            resultados = pool.map(cpu_task, [N] * TAREAS)
        t_par = time.time() - inicio
        speedup = t_seq / t_par
        print(f"Pool({workers}):    {t_par:.2f}s  (speedup: {speedup:.2f}x)")


if __name__ == "__main__":
    main()
