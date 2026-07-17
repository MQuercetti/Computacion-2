#!/usr/bin/env python3
"""
mmap_archivo.py - Ejercicio 1.1 de mmap.

Crea un archivo, lo mapea con mmap, lee su contenido, busca texto
y lo modifica. Los cambios en memoria se reflejan en el archivo.

Prerequisito: solo Linux/macOS.
"""
import mmap


ARCHIVO = "/tmp/mmap_test.txt"


def main():
    # Crear archivo con contenido
    with open(ARCHIVO, "wb") as f:
        f.write(b"Linea 1: Hola mundo\n")
        f.write(b"Linea 2: Computacion II\n")
        f.write(b"Linea 3: mmap es genial\n")

    with open(ARCHIVO, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)

        print("=== Contenido completo ===")
        print(mm[:].decode())

        print("=== Línea por línea ===")
        mm.seek(0)
        while True:
            linea = mm.readline()
            if not linea:
                break
            print(f"  {linea.decode().strip()}")

        pos = mm.find(b"mmap")
        print(f"\n'mmap' encontrado en posición: {pos}")

        # Modificar esa parte
        mm.seek(pos)
        mm.write(b"MMAP")

        mm.seek(0)
        print(f"\n=== Después de modificar ===")
        print(mm[:].decode())

        mm.close()


if __name__ == "__main__":
    main()
