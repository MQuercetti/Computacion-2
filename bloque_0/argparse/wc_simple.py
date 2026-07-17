#!/usr/bin/env python3
"""
wc_simple.py - Ejercicio 1.3 de argparse (antes vivía dentro de listar.py).

Cuenta la cantidad de líneas de un archivo de texto.
"""
import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cuenta la cantidad de líneas de un archivo."
    )
    parser.add_argument("archivo", help="Ruta del archivo a leer")
    return parser.parse_args()


def contar_lineas(ruta):
    """Devuelve la cantidad de líneas del archivo o None si falló."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return sum(1 for _ in archivo)
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta}' no existe", file=sys.stderr)
        return None
    except PermissionError:
        print(f"Error: No tiene permisos para leer '{ruta}'", file=sys.stderr)
        return None
    except OSError as error:
        print(f"Error: No se puede leer '{ruta}': {error}", file=sys.stderr)
        return None


def main():
    args = parse_args()
    cantidad = contar_lineas(args.archivo)
    if cantidad is None:
        sys.exit(1)
    print(f"{cantidad} líneas")


if __name__ == "__main__":
    main()
