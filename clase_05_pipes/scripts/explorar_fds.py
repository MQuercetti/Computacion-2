#!/usr/bin/env python3
"""
explorar_fds.py - Ejercicio 1.2 de Pipes.

Lista los file descriptors abiertos del proceso actual leyendo
/proc/<pid>/fd. Después abre dos archivos y muestra cómo aparecen
nuevos fds, los cierra y los ve desaparecer.

Prerequisito: solo Linux.
"""
import os


def listar_fds():
    """Muestra los FDs abiertos del proceso actual."""
    pid = os.getpid()
    fd_dir = f"/proc/{pid}/fd"
    print(f"File descriptors de PID {pid}:")
    for fd in sorted(os.listdir(fd_dir), key=int):
        try:
            target = os.readlink(f"{fd_dir}/{fd}")
            print(f"  fd {fd} -> {target}")
        except OSError as e:
            print(f"  fd {fd} -> (error: {e})")


def main():
    print("=== Estado inicial ===")
    listar_fds()

    print("\n=== Después de abrir un archivo ===")
    f = open("/tmp/test_fd.txt", "w")
    print(f"Archivo abierto con fd {f.fileno()}")
    listar_fds()

    print("\n=== Después de abrir otro ===")
    f2 = open("/etc/passwd", "r")
    print(f"Segundo archivo con fd {f2.fileno()}")
    listar_fds()

    print("\n=== Después de cerrar el primero ===")
    f.close()
    listar_fds()

    print("\n=== Después de cerrar todo ===")
    f2.close()
    listar_fds()


if __name__ == "__main__":
    main()
