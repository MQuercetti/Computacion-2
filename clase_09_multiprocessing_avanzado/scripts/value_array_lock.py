#!/usr/bin/env python3
"""
value_array_lock.py - Ejercicio 3 de Multiprocessing avanzado.

Memoria compartida con Value (con get_lock) y Array particionado.
4 procesos incrementan un Value; otros 4 llenan su segmento de un Array.

Prerequisito: funciona en Linux/macOS/Windows.
"""
from multiprocessing import Array, Process, Value


def incrementar(contador, n_veces, id):
    for _ in range(n_veces):
        with contador.get_lock():
            contador.value += 1
    print(f"Worker {id} terminó sus {n_veces} incrementos", flush=True)


def llenar_array(arr, valor_inicial, id):
    """Cada worker llena su segmento del array."""
    inicio = id * (len(arr) // 4)
    fin = inicio + (len(arr) // 4)
    for i in range(inicio, fin):
        arr[i] = valor_inicial + i


def main():
    # Value compartido con auto-lock
    contador = Value('i', 0)
    procs = [Process(target=incrementar, args=(contador, 10_000, i)) for i in range(4)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print(f"\nContador final: {contador.value}")
    assert contador.value == 40_000, "Race condition sin lock"

    # Array compartido, particionado por worker
    arr = Array('i', 100)
    procs = [Process(target=llenar_array, args=(arr, 1000, i)) for i in range(4)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print(f"Array completo (primeros 10): {list(arr)[:10]}")
    print(f"Array completo (últimos 10): {list(arr)[-10:]}")


if __name__ == "__main__":
    main()
