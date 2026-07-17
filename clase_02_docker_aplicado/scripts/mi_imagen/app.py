#!/usr/bin/env python3
"""
app.py - Ejercicio 3.1 de Docker Aplicado.

Imprime un mensaje con cowsay. Se usa como aplicación dentro de
un contenedor Docker construido con el Dockerfile de esta carpeta.
"""
import sys

import cowsay


def main():
    mensaje = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hola Docker!"
    cowsay.cow(mensaje)


if __name__ == "__main__":
    main()
