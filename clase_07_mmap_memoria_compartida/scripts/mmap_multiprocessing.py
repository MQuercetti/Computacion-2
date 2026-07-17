#!/usr/bin/env python3
"""
mmap_multiprocessing.py - Ejercicio 4.1 de mmap.

Usa mmap con multiprocessing.Process. Cada proceso abre el mismo
archivo, escribe un mensaje en su offset y el padre lee todo al final.

Prerequisito: solo Linux/macOS/Windows (mmap de archivo funciona en todos).
"""
import mmap
import os
import struct
from multiprocessing import Process


ARCHIVO = "/tmp/mmap_mp.bin"
TAMANO = 256


def escribir_en_mmap(archivo, offset, mensaje):
    """Cada proceso abre el archivo y escribe en su offset."""
    with open(archivo, "r+b") as f:
        mm = mmap.mmap(f.fileno(), TAMANO)
        encoded = mensaje.encode()
        struct.pack_into('i', mm, offset, len(encoded))
        mm[offset+4:offset+4+len(encoded)] = encoded
        mm.close()


def main():
    with open(ARCHIVO, "wb") as f:
        f.write(b'\x00' * TAMANO)

    mensajes = [
        "Hola desde proceso 0",
        "Saludos del proceso 1",
        "Proceso 2 presente",
        "Proceso 3 reportando",
    ]

    procesos = [
        Process(target=escribir_en_mmap, args=(ARCHIVO, i * 64, msg))
        for i, msg in enumerate(mensajes)
    ]
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()

    with open(ARCHIVO, "r+b") as f:
        mm = mmap.mmap(f.fileno(), TAMANO)
        print("=== Mensajes de los procesos ===")
        for i in range(4):
            offset = i * 64
            largo = struct.unpack_from('i', mm, offset)[0]
            if largo > 0:
                msg = bytes(mm[offset+4:offset+4+largo]).decode()
                print(f"  Proceso {i}: {msg}")
        mm.close()

    os.unlink(ARCHIVO)


if __name__ == "__main__":
    main()
