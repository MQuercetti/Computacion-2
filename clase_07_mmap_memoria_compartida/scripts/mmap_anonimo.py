#!/usr/bin/env python3
"""
mmap_anonimo.py - Ejercicio 3.1 de mmap.

mmap anónimo (sin archivo) entre padre e hijo vía fork. El hijo
escribe un entero y un string; el padre los lee.

Prerequisito: solo Linux/macOS.
"""
import mmap
import os
import struct


def main():
    mm = mmap.mmap(-1, 256)  # -1 = anónimo

    pid = os.fork()

    if pid == 0:
        print(f"[HIJO {os.getpid()}] Escribiendo datos...", flush=True)

        struct.pack_into('i', mm, 0, 42)

        mensaje = b"Hola desde el hijo!"
        struct.pack_into('i', mm, 4, len(mensaje))
        mm[8:8+len(mensaje)] = mensaje

        print("[HIJO] Datos escritos, terminando", flush=True)
        os._exit(0)

    else:
        os.wait()
        print(f"[PADRE] Hijo terminó, leyendo datos...", flush=True)

        numero = struct.unpack_from('i', mm, 0)[0]
        print(f"[PADRE] Número: {numero}", flush=True)

        largo = struct.unpack_from('i', mm, 4)[0]
        mensaje = bytes(mm[8:8+largo]).decode()
        print(f"[PADRE] Mensaje: {mensaje}", flush=True)

        mm.close()


if __name__ == "__main__":
    main()
