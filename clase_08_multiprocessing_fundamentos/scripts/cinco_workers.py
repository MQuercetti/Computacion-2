#!/usr/bin/env python3
"""
cinco_workers.py - Ejercicio 2 de Multiprocessing fundamentos.

Lanza 5 workers en paralelo. Cada uno duerme un tiempo random.
Mide el tiempo total: debería ser ~max(tiempos), no la suma.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import random
import time
from multiprocessing import Process


def worker(worker_id, duraciones, start):
    """Espera hasta que start esté dado, luego duerme duraciones[id]."""
    while time.perf_counter() < start:
        time.sleep(0.001)
    time.sleep(duraciones[worker_id])
    print(f"[Worker {worker_id}] terminó en {duraciones[worker_id]:.1f}s", flush=True)


def main():
    NUM = 5
    duraciones = [random.uniform(0.5, 2.0) for _ in range(NUM)]
    print(f"Duraciones: {[round(d, 1) for d in duraciones]}")

    # Sincronizar inicio: todos arrancan a la vez
    start = time.perf_counter() + 0.5

    t0 = time.perf_counter()
    procesos = [Process(target=worker, args=(i, duraciones, start)) for i in range(NUM)]
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()
    t_total = time.perf_counter() - t0

    print(f"\nTiempo total: {t_total:.2f}s (suma de duraciones: {sum(duraciones):.2f}s)")


if __name__ == "__main__":
    main()
