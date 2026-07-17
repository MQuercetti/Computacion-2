#!/usr/bin/env python3
"""
n_hijos.py - Ejercicio 2 de Procesos - fork, exec, wait.

Crea 5 hijos con os.fork(). Cada hijo duerme un tiempo aleatorio
y termina con un exit code igual a su número. El padre espera a
todos y reporta el exit code de cada uno.

Prerequisito: solo Linux/macOS.
"""
import os
import random
import time


def main():
    hijos = []  # lista de (pid, numero)
    for i in range(5):
        pid = os.fork()
        if pid == 0:
            # Hijo
            duracion = random.uniform(0.5, 2)
            print(f"[Hijo {i}] PID={os.getpid()}, dormiré {duracion:.1f}s")
            time.sleep(duracion)
            os._exit(i)
        else:
            # Padre
            hijos.append((pid, i))

    for pid, i in hijos:
        _, status = os.waitpid(pid, 0)
        codigo = os.WEXITSTATUS(status)
        print(f"Hijo {i} (PID {pid}) terminó con código {codigo}")


if __name__ == "__main__":
    main()
