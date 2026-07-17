#!/usr/bin/env python3
"""
inspeccionar_proceso.py - Ejercicio 1 de Procesos - Fundamentos.

Muestra información del proceso actual leída desde /proc:
- PID y PPID
- Working directory
- File descriptors abiertos
- Primeras líneas del mapa de memoria

Prerequisito: solo funciona en Linux (lee /proc/<pid>/...).
"""
import os
import sys


def listar_fds(pid):
    """Itera sobre /proc/<pid>/fd y muestra el destino de cada FD."""
    fd_dir = f"/proc/{pid}/fd"
    for fd in sorted(os.listdir(fd_dir), key=int):
        try:
            link = os.readlink(f"{fd_dir}/{fd}")
            print(f"  fd {fd} -> {link}")
        except OSError:
            pass


def mostrar_mapa(pid, n=20):
    """Muestra las primeras n líneas de /proc/<pid>/maps."""
    with open(f"/proc/{pid}/maps", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            print(f"  {line.rstrip()}")


def main():
    pid = os.getpid()
    print(f"PID: {pid}")
    print(f"PPID: {os.getppid()}")
    print(f"CWD: {os.getcwd()}")

    print("\nFile descriptors abiertos:")
    try:
        listar_fds(pid)
    except OSError as e:
        print(f"  (no se pudo listar: {e})", file=sys.stderr)

    print("\nMapa de memoria (primeras 20 líneas):")
    try:
        mostrar_mapa(pid)
    except OSError as e:
        print(f"  (no se pudo leer: {e})", file=sys.stderr)


if __name__ == "__main__":
    main()
