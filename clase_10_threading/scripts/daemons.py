#!/usr/bin/env python3
"""
daemons.py - Ejercicio 6 de Threading.

Hilos daemon vs no-daemon. Los daemons mueren cuando el main termina.
Los no-daemon siguen vivos y mantienen el programa corriendo.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import threading
import time


def loop_infinito(label):
    while True:
        print(f"[{label}] trabajando...", flush=True)
        time.sleep(1)


def main():
    # Daemon: el main termina y el hilo muere
    h = threading.Thread(target=loop_infinito, args=("daemon",), daemon=True)
    h.start()

    time.sleep(3)
    print("Main terminó: el daemon muere automáticamente")


if __name__ == "__main__":
    main()
