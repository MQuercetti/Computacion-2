#!/usr/bin/env python3
"""
ctrl_c_handler.py - Ejercicio 2.1 de Señales.

Captura SIGINT (Ctrl+C) con un handler. La primera vez ignora,
la segunda también, a la tercera termina.

Probalo: ejecutá el script y presioná Ctrl+C varias veces.
"""
import signal
import time


def main():
    contador = 0

    def handler(sig, frame):
        nonlocal contador
        contador += 1
        print(f"\n¡Ctrl+C detectado! (vez #{contador})", flush=True)
        if contador >= 3:
            print("OK, OK, me voy...")
            raise SystemExit(0)
        else:
            print(f"Presioná {3 - contador} veces más para salir", flush=True)

    signal.signal(signal.SIGINT, handler)
    print("Presioná Ctrl+C (3 veces para salir)")
    print("Observá cómo el programa no termina las primeras veces")

    while True:
        print(".", end="", flush=True)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
