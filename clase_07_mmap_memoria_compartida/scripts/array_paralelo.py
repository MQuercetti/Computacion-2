#!/usr/bin/env python3
"""
array_paralelo.py - Ejercicio 5.2 de mmap.

Cálculo paralelo usando Array compartido de multiprocessing.
4 procesos calculan el cuadrado de su porción del array.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import time
from multiprocessing import Array, Process


def calcular_rango(resultado, inicio, fin):
    """Calcula el cuadrado de cada índice en [inicio, fin)."""
    for i in range(inicio, fin):
        resultado[i] = i * i


def main():
    TAMANO = 1000
    resultado = Array('i', TAMANO)

    NUM_PROCESOS = 4
    chunk = TAMANO // NUM_PROCESOS

    inicio = time.time()
    procesos = []
    for i in range(NUM_PROCESOS):
        ini = i * chunk
        fin = (i + 1) * chunk if i < NUM_PROCESOS - 1 else TAMANO
        p = Process(target=calcular_rango, args=(resultado, ini, fin))
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()

    duracion = time.time() - inicio

    print(f"Cálculo completado en {duracion:.4f}s")
    print(f"resultado[0] = {resultado[0]}")
    print(f"resultado[10] = {resultado[10]}")
    print(f"resultado[99] = {resultado[99]}")
    print(f"resultado[999] = {resultado[999]}")

    errores = sum(1 for i in range(TAMANO) if resultado[i] != i * i)
    print(f"Errores: {errores}")


if __name__ == "__main__":
    main()
