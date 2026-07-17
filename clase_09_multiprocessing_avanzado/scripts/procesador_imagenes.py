#!/usr/bin/env python3
"""
procesador_imagenes.py - Ejercicio 5 (OBLIGATORIO) de Multiprocessing avanzado.

Procesador de imágenes en paralelo. Aplica un blur 3x3 a N imágenes
(matrices de enteros) y compara tiempo secuencial vs paralelo con Pool.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import random
import time
from multiprocessing import Pool


def crear_imagen(size):
    """Crea una 'imagen' como lista de listas."""
    return [[random.randint(0, 255) for _ in range(size)] for _ in range(size)]


def aplicar_filtro(imagen):
    """Aplica un filtro blur 3x3 (CPU-intensive)."""
    size = len(imagen)
    resultado = [[0] * size for _ in range(size)]
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            suma = 0
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    suma += imagen[i + di][j + dj]
            resultado[i][j] = suma // 9
    return resultado


def procesar_imagen(args):
    idx, imagen = args
    inicio = time.time()
    resultado = aplicar_filtro(imagen)
    duracion = time.time() - inicio
    return idx, duracion, sum(sum(row) for row in resultado)


def main():
    NUM_IMAGENES = 8
    SIZE = 100

    print(f"Creando {NUM_IMAGENES} imágenes de {SIZE}x{SIZE}...", flush=True)
    imagenes = [(i, crear_imagen(SIZE)) for i in range(NUM_IMAGENES)]

    print("\nProcesamiento secuencial:", flush=True)
    inicio = time.time()
    for img in imagenes:
        procesar_imagen(img)
    t_secuencial = time.time() - inicio
    print(f"Tiempo: {t_secuencial:.2f}s", flush=True)

    print("\nProcesamiento paralelo (4 workers):", flush=True)
    inicio = time.time()
    with Pool(4) as pool:
        resultados = pool.map(procesar_imagen, imagenes)
    t_paralelo = time.time() - inicio

    for idx, duracion, checksum in resultados:
        print(f"  Imagen {idx}: {duracion:.3f}s", flush=True)

    print(f"Tiempo total: {t_paralelo:.2f}s", flush=True)
    print(f"Speedup: {t_secuencial / t_paralelo:.2f}x", flush=True)


if __name__ == "__main__":
    main()
