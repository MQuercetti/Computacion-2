#!/usr/bin/env python3
"""
fork_exec_launcher.py - Ejercicio 3 de Procesos - fork, exec, wait.

Implementa el patrón fork-exec: el padre hace fork, el hijo hace exec
del comando externo, el padre espera y reporta el exit code.

Prerequisito: solo Linux/macOS.
"""
import os
import sys


def lanzar(comando, args):
    """Hace fork+exec+wait y devuelve el exit code del comando."""
    pid = os.fork()
    if pid == 0:
        # Hijo: reemplaza su imagen con el comando
        os.execvp(comando, [comando] + args)
        # Si llegamos aquí, exec falló
        print(f"Error: no se pudo ejecutar {comando}", file=sys.stderr)
        os._exit(127)
    else:
        # Padre: espera al hijo
        _, status = os.waitpid(pid, 0)
        return os.WEXITSTATUS(status)


def main():
    if len(sys.argv) < 2:
        print("Uso: python fork_exec_launcher.py <comando> [args...]", file=sys.stderr)
        sys.exit(2)

    codigo = lanzar(sys.argv[1], sys.argv[2:])
    print(f"Comando terminó con código {codigo}")
    sys.exit(codigo)


if __name__ == "__main__":
    main()
