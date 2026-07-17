#!/usr/bin/env python3
"""
primer_hilo.py - Ejercicio 1 de Threading.

Crea 3 hilos que imprimen números 1-5 con pausas. El programa
principal espera a que todos terminen.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import threading
import time


def imprimir_numeros(nombre):
    for i in range(1, 6):
        print(f"[{nombre}] número: {i}", flush=True)
        time.sleep(0.2)


def main():
    hilos = [
        threading.Thread(target=imprimir_numeros, args=(f"Hilo-{i}",))
        for i in range(1, 4)
    ]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    print("Listo")


if __name__ == "__main__":
    main()
