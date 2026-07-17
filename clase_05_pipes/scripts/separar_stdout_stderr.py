#!/usr/bin/env python3
"""
separar_stdout_stderr.py - Ejercicio 2.2 de Pipes.

Muestra cómo se separan stdout y stderr. Probalo con:

    python3 separar_salidas.py > solo_stdout.txt
    python3 separar_salidas.py 2> solo_stderr.txt
    python3 separar_salidas.py > stdout.txt 2> stderr.txt
    python3 separar_salidas.py > todo.txt 2>&1
"""
import os
import sys


def main():
    # stdout (fd 1)
    print("Mensaje normal a stdout")
    sys.stdout.write("Otro mensaje a stdout\n")
    os.write(1, b"Y otro mas directo al fd 1\n")

    # stderr (fd 2)
    print("Mensaje de error a stderr", file=sys.stderr)
    sys.stderr.write("Otro error a stderr\n")
    os.write(2, b"Error directo al fd 2\n")


if __name__ == "__main__":
    main()
