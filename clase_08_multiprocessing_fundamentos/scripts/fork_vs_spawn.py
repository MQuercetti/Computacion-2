#!/usr/bin/env python3
"""
fork_vs_spawn.py - Ejercicio 5 de Multiprocessing fundamentos.

Compara el tiempo de creación de 100 procesos con start_method='fork'
vs 'spawn'. En Linux el fork es más rápido (no reimporta el módulo).
En Windows solo está disponible spawn.

Prerequisito: solo Linux/macOS para fork. Windows solo spawn.
"""
import os
import time
import multiprocessing as mp


def noop(_):
    """Función vacía: solo queremos medir el overhead de crear el proceso."""
    pass


def medir(metodo, n):
    ctx = mp.get_context(metodo)
    t0 = time.perf_counter()
    procesos = [ctx.Process(target=noop, args=(i,)) for i in range(n)]
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()
    return time.perf_counter() - t0


def main():
    if os.name == "posix":
        # Linux/macOS: podemos fork y spawn
        t_fork = medir("fork", 100)
        print(f"fork:  {t_fork:.3f}s para 100 procesos")

        t_spawn = medir("spawn", 100)
        print(f"spawn: {t_spawn:.3f}s para 100 procesos")
        print(f"fork es {t_spawn / t_fork:.1f}x más rápido")
    else:
        # Windows: solo spawn
        t = medir("spawn", 100)
        print(f"spawn: {t:.3f}s para 100 procesos (Windows solo soporta spawn)")


if __name__ == "__main__":
    main()
