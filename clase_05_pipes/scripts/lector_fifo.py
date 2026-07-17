#!/usr/bin/env python3
"""
lector_fifo.py - Ejercicio 7.1 de Pipes (lector).

Lee mensajes de un named pipe (FIFO). Ejecutar en otra terminal
después de lanzar escritor_fifo.py.

Prerequisito: solo Linux/macOS.
"""
FIFO = "/tmp/mi_canal"


def main():
    print(f"Leyendo de {FIFO}...")

    with open(FIFO, "r", encoding="utf-8") as f:
        for linea in f:
            print(f"Recibido: {linea.strip()}")

    print("Lectura completada (el escritor cerró el pipe)")


if __name__ == "__main__":
    main()
