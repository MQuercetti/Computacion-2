#!/usr/bin/env python3
"""
info_sistema.py - Ejercicio de síntesis de Docker Intro.

Muestra información del sistema: Python, OS, CPUs, memoria y vars
de entorno que empiecen con PYTHON. Pensado para comparar la salida
corrida en local, en python:3.11 y en python:3.9 (ejercicio final
de la clase).

Uso:
    python info_sistema.py
    docker run -v $(pwd):/app -w /app python:3.11 python info_sistema.py
    docker run -v $(pwd):/app -w /app python:3.9 python info_sistema.py
"""
import os
import platform
import sys


def memoria_disponible():
    """Devuelve memoria disponible en MB o None si no se puede obtener."""
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.startswith("MemAvailable:"):
                    kb = int(linea.split()[1])
                    return kb / 1024  # MB
    except (OSError, ValueError):
        return None
    return None


def cpus_disponibles():
    """Devuelve la cantidad de CPUs disponibles."""
    return os.cpu_count() or 1


def vars_python():
    """Devuelve las variables de entorno que empiezan con PYTHON."""
    prefijo = "PYTHON"
    return {
        clave: valor
        for clave, valor in os.environ.items()
        if clave.upper().startswith(prefijo)
    }


def main():
    print("=" * 60)
    print("Información del sistema")
    print("=" * 60)

    print(f"Python: {sys.version.splitlines()[0]}")
    print(f"Implementación: {platform.python_implementation()}")
    print(f"Compilación: {platform.python_compiler() or 'desconocida'}")

    print(f"\nSistema operativo: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Versión: {platform.version()}")
    print(f"Arquitectura: {platform.machine()}")

    print(f"\nCPUs disponibles: {cpus_disponibles()}")

    memoria = memoria_disponible()
    if memoria is None:
        print("Memoria disponible: no se pudo determinar (no es Linux o falta /proc)")
    else:
        print(f"Memoria disponible: {memoria:.0f} MB")

    variables = vars_python()
    print(f"\nVariables de entorno que empiezan con PYTHON: {len(variables)}")
    if variables:
        for clave in sorted(variables):
            print(f"  {clave} = {variables[clave]}")
    else:
        print("  (ninguna)")

    print("=" * 60)


if __name__ == "__main__":
    main()
