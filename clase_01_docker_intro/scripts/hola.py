#!/usr/bin/env python3
"""
hola.py - Ejercicio 3.1 de Docker Intro.

Script de prueba que muestra información del entorno donde se ejecuta.
Pensado para correr dentro de un contenedor Docker con:

    docker run -v $(pwd):/app -w /app python python hola.py
"""
import os
import platform
import sys
from datetime import datetime


def info_sistema():
    """Devuelve tuplas (sistema, hostname) portable."""
    sistema = platform.system()
    hostname = platform.node()
    return sistema, hostname


def main():
    print("=" * 50)
    print("Ejecutando en Docker")
    print("=" * 50)
    print(f"Python: {sys.version.splitlines()[0]}")
    sistema, hostname = info_sistema()
    print(f"Sistema: {sistema}")
    print(f"Hostname: {hostname}")
    print(f"Fecha: {datetime.now().isoformat()}")
    print(f"Usuario: {os.getenv('USER') or os.getenv('USERNAME', 'desconocido')}")
    print(f"Directorio actual: {os.getcwd()}")
    try:
        print(f"Archivos aquí: {os.listdir('.')}")
    except OSError as error:
        print(f"No se pudo listar el directorio: {error}")
    print("=" * 50)


if __name__ == "__main__":
    main()
