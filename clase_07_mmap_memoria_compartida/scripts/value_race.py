#!/usr/bin/env python3
"""
value_race.py - Ejercicio 5.1 de mmap.

Demuestra una race condition con multiprocessing.Value.
4 procesos incrementan un Value 100.000 veces cada uno.
Sin lock, el valor final siempre es menor que 400.000.

Prerequisito: solo Linux/macOS/Windows (multiprocessing funciona en todos).
"""
import time
from multiprocessing import Process, Value


def incrementar(contador, n, nombre):
    """Incrementa el contador n veces sin lock."""
    print(f"[{nombre}] Iniciando {n} incrementos...", flush=True)
    for _ in range(n):
        contador.value += 1
    print(f"[{nombre}] Terminado", flush=True)


def main():
    contador = Value('i', 0)

    N = 100_000
    procesos = []
    for i in range(4):
        p = Process(target=incrementar, args=(contador, N, f"P{i}"))
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()

    esperado = 4 * N
    print(f"\nEsperado: {esperado}")
    print(f"Obtenido: {contador.value}")
    print(f"Diferencia: {esperado - contador.value} (incrementos perdidos)")


if __name__ == "__main__":
    main()
