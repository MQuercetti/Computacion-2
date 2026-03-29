#1.3
import sys
import argparse

parser = argparse.ArgumentParser(description="Cuenta la cantidad de lineas de un archivo")
parser.add_argument("archivo", help="Ruta del archivo a leer")
args = parser.parse_args()

nombre_archivo = args.archivo

try:
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        cantidad_lineas = sum(1 for _ in archivo)

    print(f"{cantidad_lineas} lineas")
except FileNotFoundError:
    print(f"Error: El archivo '{nombre_archivo}' no existe")
    sys.exit(1)
except PermissionError:
    print(f"Error: No tiene permisos para leer '{nombre_archivo}'")
    sys.exit(1)
except OSError:
    print(f"Error: No se puede leer '{nombre_archivo}'")
    sys.exit(1)