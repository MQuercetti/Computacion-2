#!/usr/bin/env python3
"""
con_dependencias.py - Ejercicio 5.1 de Docker Intro.

Script que usa una biblioteca externa (requests) para hacer un GET.
La imagen base de Python no trae requests instalado, por eso falla
al correr tal cual. La idea es instalarlo dentro del contenedor:

    docker run -v $(pwd):/app -w /app python \\
        sh -c "pip install requests && python con_dependencias.py"
"""
import sys

try:
    import requests
except ImportError:
    print(
        "Error: la biblioteca 'requests' no está instalada.\n"
        "Instalala con: pip install requests",
        file=sys.stderr,
    )
    sys.exit(1)


def main():
    response = requests.get("https://httpbin.org/get", timeout=10)
    print(f"Status: {response.status_code}")
    payload = response.json()
    print(f"Origen: {payload.get('origin', 'desconocido')}")


if __name__ == "__main__":
    main()
