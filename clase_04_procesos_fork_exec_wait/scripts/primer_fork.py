#!/usr/bin/env python3
"""
primer_fork.py - Ejercicio 1 de Procesos - fork, exec, wait.

Hace os.fork() y muestra el doble flujo de ejecución.
El padre espera al hijo antes de terminar.

Prerequisito: solo corre en Linux/macOS (fork no existe en Windows).
Para correr en Windows usá un contenedor Docker:

    docker run -it --rm -v $(pwd):/app -w /app python:3.11 python primer_fork.py
"""
import os


def main():
    pid = os.fork()

    if pid == 0:
        # Rama del hijo
        print(f"Soy el hijo: PID={os.getpid()}, padre={os.getppid()}")
        os._exit(0)
    else:
        # Rama del padre
        print(f"Soy el padre: PID={os.getpid()}, hijo={pid}")
        os.wait()
        print("Programa terminado")


if __name__ == "__main__":
    main()
