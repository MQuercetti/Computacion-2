#!/usr/bin/env python3
"""
mmap_readonly.py - Ejercicio 1.2 de mmap.

Mapea un archivo en modo solo lectura. Intentar escribir tira TypeError.

Prerequisito: solo Linux/macOS.
"""
import mmap


ARCHIVO = "/tmp/mmap_test.txt"


def main():
    with open(ARCHIVO, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        print(f"Contenido: {mm[:40]}")
        print(f"Tamaño: {mm.size()} bytes")

        try:
            mm[0:4] = b"TEST"
        except TypeError as e:
            print(f"Error al escribir (esperado): {e}")

        mm.close()


if __name__ == "__main__":
    main()
