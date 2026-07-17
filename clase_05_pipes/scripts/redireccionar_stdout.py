#!/usr/bin/env python3
"""
redireccionar_stdout.py - Ejercicio 2.1 de Pipes.

Redirige stdout a un archivo usando os.dup2 (sin la sintaxis del shell).
Después restaura stdout a la terminal.

Prerequisito: solo Linux/macOS.
"""
import os
import sys


def main():
    print("Este mensaje va a la terminal")

    # Guardar stdout original
    stdout_original = os.dup(1)

    # Abrir archivo destino
    archivo = os.open("/tmp/salida.txt", os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)

    # Redirigir stdout al archivo
    os.dup2(archivo, 1)
    os.close(archivo)

    # Estos prints van al archivo, no a la pantalla
    print("Este mensaje va al archivo")
    print("Y este también")
    sys.stdout.flush()

    # Restaurar stdout a la terminal
    os.dup2(stdout_original, 1)
    os.close(stdout_original)

    print("Volvimos a la terminal")
    print("Revisá el contenido de /tmp/salida.txt")


if __name__ == "__main__":
    main()
