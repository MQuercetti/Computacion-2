#!/usr/bin/env python3
"""
mmap_binario.py - Ejercicio 2.1 de mmap.

Usa mmap como almacenamiento binario estructurado con struct.pack_into
y struct.unpack_from. Almacena enteros de 4 bytes.

Prerequisito: solo Linux/macOS.
"""
import mmap
import os
import struct


ARCHIVO = "/tmp/numeros.bin"
NUM_ELEMENTOS = 10
TAMANO = NUM_ELEMENTOS * 4  # 4 bytes por entero


def main():
    # Crear archivo con tamaño fijo
    with open(ARCHIVO, "wb") as f:
        f.write(b'\x00' * TAMANO)

    with open(ARCHIVO, "r+b") as f:
        mm = mmap.mmap(f.fileno(), TAMANO)

        print("Escribiendo números...")
        for i in range(NUM_ELEMENTOS):
            valor = (i + 1) * 100
            struct.pack_into('i', mm, i * 4, valor)
            print(f"  Posición {i}: {valor}")

        print("\nLeyendo números...")
        for i in range(NUM_ELEMENTOS):
            valor = struct.unpack_from('i', mm, i * 4)[0]
            print(f"  Posición {i}: {valor}")

        struct.pack_into('i', mm, 3 * 4, 9999)
        print(f"\nPosición 3 modificada a: {struct.unpack_from('i', mm, 3 * 4)[0]}")

        mm.close()

    os.unlink(ARCHIVO)


if __name__ == "__main__":
    main()
