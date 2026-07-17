#!/usr/bin/env python3
"""
red_basica.py - Ejercicio 2.1 de Docker Aplicado.

Pequeño test que intenta resolver un nombre DNS de un contenedor
hermano en una red Docker personalizada. Pensado para correr dentro
de un contenedor en la red `ejercicio-red` con un contenedor llamado
`servidor` que escucha en el puerto 8000.

    docker run --rm --network ejercicio-red python:3.11 python red_basica.py
"""
import socket
import sys
import urllib.request

HOST = "servidor"
PORT = 8000


def resolver():
    """Intenta resolver el nombre de host a una IP."""
    try:
        ip = socket.gethostbyname(HOST)
    except socket.gaierror as e:
        print(f"No se pudo resolver {HOST}: {e}", file=sys.stderr)
        return None
    print(f"{HOST} -> {ip}")
    return ip


def fetch():
    """Hace un GET a http://servidor:8000/ y muestra los primeros bytes."""
    try:
        with urllib.request.urlopen(f"http://{HOST}:{PORT}/", timeout=5) as resp:
            data = resp.read(100)
            print(f"Status: {resp.status}")
            print(f"Primeros 100 bytes: {data!r}")
    except Exception as e:
        print(f"Error al hacer fetch: {e}", file=sys.stderr)


if __name__ == "__main__":
    if resolver() is not None:
        fetch()
