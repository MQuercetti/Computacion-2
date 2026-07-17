#!/usr/bin/env python3
"""
mayusculas.py - Ejercicio 6.1 de Pipes.

Filtro Unix: lee stdin, escribe stdout, pero en mayúsculas.

Probalo:
    echo "hola mundo" | python3 mayusculas.py
    cat archivo.txt | python3 mayusculas.py | head -5
"""
import sys


def main():
    for linea in sys.stdin:
        sys.stdout.write(linea.upper())


if __name__ == "__main__":
    main()
