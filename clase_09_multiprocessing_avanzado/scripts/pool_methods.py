#!/usr/bin/env python3
"""
pool_methods.py - Ejercicio 1 de Multiprocessing avanzado.

Explora los distintos métodos de Pool: map, imap, imap_unordered,
starmap, apply_async. La función cuadrado tiene duración variable
para que se vean las diferencias de orden.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import random
import time
from multiprocessing import Pool


def cuadrado(x):
    """Tarea con duración variable."""
    duracion = random.uniform(0.1, 1.0)
    time.sleep(duracion)
    return x ** 2


def suma(a, b):
    return a + b


def main():
    with Pool(4) as pool:
        # map: síncrono, ordenado
        print("== map ==")
        print(pool.map(cuadrado, range(8)))

        # map_async
        print("\n== map_async ==")
        async_result = pool.map_async(cuadrado, range(8))
        print(f"ready inmediatamente? {async_result.ready()}")
        print(f"resultados: {async_result.get()}")

        # imap: iterador lazy, mantiene orden
        print("\n== imap (mantiene orden) ==")
        for r in pool.imap(cuadrado, range(8)):
            print(f"  llegó: {r}")

        # imap_unordered: lazy, sin orden
        print("\n== imap_unordered (orden de finalización) ==")
        for r in pool.imap_unordered(cuadrado, range(8)):
            print(f"  llegó: {r}")

        # starmap: múltiples args
        print("\n== starmap ==")
        print(pool.starmap(suma, [(1, 2), (3, 4), (5, 6)]))

        # apply_async: control fino
        print("\n== apply_async ==")
        resultado = pool.apply_async(cuadrado, (10,))
        print(f"ready? {resultado.ready()}")
        print(f"resultado: {resultado.get()}")


if __name__ == "__main__":
    main()
