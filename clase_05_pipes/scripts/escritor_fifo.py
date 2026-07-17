#!/usr/bin/env python3
"""
escritor_fifo.py - Ejercicio 7.1 de Pipes (escritor).

Escribe mensajes a un named pipe (FIFO). Ejecutar en una terminal.
En otra terminal, correr lector_fifo.py.

Prerequisito: solo Linux/macOS.
"""
import os
import time

FIFO = "/tmp/mi_canal"


def main():
    if not os.path.exists(FIFO):
        os.mkfifo(FIFO)

    print(f"Escribiendo a {FIFO}...")
    print("(Ejecutá lector_fifo.py en otra terminal)")

    with open(FIFO, "w", encoding="utf-8") as f:
        for i in range(10):
            mensaje = f"Mensaje {i}: {time.ctime()}"
            print(f"Enviando: {mensaje}")
            f.write(mensaje + "\n")
            f.flush()
            time.sleep(1)

    print("Escritura completada")


if __name__ == "__main__":
    main()
