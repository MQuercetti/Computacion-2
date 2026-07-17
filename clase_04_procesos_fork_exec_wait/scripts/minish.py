#!/usr/bin/env python3
"""
minish.py - Ejercicio 5 (OBLIGATORIO) de Procesos - fork, exec, wait.

Mini-shell minimalista que implementa el patrón fork-exec.
Soporta:
- cd (sin fork, porque debe cambiar el shell mismo)
- cualquier comando externo vía fork+exec+wait
- exit para salir

Prerequisito: solo Linux/macOS.
"""
import os
import sys


def ejecutar_externo(comando, args):
    """Hace fork+exec+wait y devuelve el exit code."""
    pid = os.fork()
    if pid == 0:
        # Hijo
        try:
            os.execvp(comando, [comando] + args)
        except OSError as e:
            print(f"minish: {comando}: {e}", file=sys.stderr)
            os._exit(127)
    else:
        # Padre
        _, status = os.waitpid(pid, 0)
        return os.WEXITSTATUS(status) if os.WIFEXITED(status) else -1


def procesar_linea(linea):
    """Parsea y ejecuta una línea. Devuelve False si hay que salir."""
    partes = linea.split()
    if not partes:
        return True

    cmd = partes[0]

    if cmd == "exit":
        return False

    if cmd == "cd":
        # cd no se hace con fork: tiene que cambiar el shell
        destino = partes[1] if len(partes) > 1 else os.environ.get("HOME", "/")
        try:
            os.chdir(destino)
        except OSError as e:
            print(f"cd: {e}", file=sys.stderr)
        return True

    # Comando externo: fork+exec+wait
    codigo = ejecutar_externo(cmd, partes[1:])
    if codigo != 0:
        print(f"minish: proceso terminó con código {codigo}", file=sys.stderr)
    return True


def main():
    while True:
        try:
            linea = input("minish$ ")
        except EOFError:
            print("\nChau!")
            break
        except KeyboardInterrupt:
            print("^C")
            continue

        linea = linea.strip()
        if not linea:
            continue

        if not procesar_linea(linea):
            break


if __name__ == "__main__":
    main()
