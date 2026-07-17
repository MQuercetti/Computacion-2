#!/usr/bin/env python3
"""
contador.py - Ejercicio 1.1 de Docker Aplicado.

Lee y actualiza un contador en /datos/contador.txt.
Pensado para correr dentro de un contenedor con un volumen bind-mounted:

    docker run -v $(pwd):/app -v $(pwd)/datos:/datos -w /app python python contador.py

Cada ejecución incrementa en 1. Como el archivo vive en el volumen,
el contador persiste entre ejecuciones.
"""
import os
from datetime import datetime

ARCHIVO = "/datos/contador.txt"


def leer_contador():
    """Lee el contador del archivo. Si no existe, devuelve 0."""
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, encoding="utf-8") as f:
            return int(f.read().strip())
    return 0


def guardar_contador(n):
    """Guarda el contador en el archivo, creando el directorio si hace falta."""
    os.makedirs(os.path.dirname(ARCHIVO), exist_ok=True)
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write(str(n))


if __name__ == "__main__":
    n = leer_contador()
    n += 1
    guardar_contador(n)
    print(f"[{datetime.now().isoformat()}] Contador: {n}")
