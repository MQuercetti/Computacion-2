#!/usr/bin/env python3
"""
race_y_lock.py - Ejercicio 5 de Threading.

Demuestra una race condition con un saldo bancario y la corrige
usando threading.Lock.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import threading
import time


def retirar_inseguro(monto, resultados, lock, idx):
    global saldo_inseguro
    if saldo_inseguro >= monto:
        time.sleep(0.001)
        saldo_inseguro -= monto


def retirar_seguro(monto, lock):
    global saldo_seguro
    with lock:
        if saldo_seguro >= monto:
            time.sleep(0.001)
            saldo_seguro -= monto


saldo_inseguro = 1000
saldo_seguro = 1000


def main():
    global saldo_inseguro, saldo_seguro

    # Versión CON race condition
    hilos = [threading.Thread(target=retirar_inseguro, args=(200, None, None, i)) for i in range(10)]
    for h in hilos: h.start()
    for h in hilos: h.join()
    print(f"Saldo inseguro final: ${saldo_inseguro} (puede ser negativo)")

    # Versión CORREGIDA con Lock
    lock = threading.Lock()
    hilos = [threading.Thread(target=retirar_seguro, args=(200, lock)) for _ in range(10)]
    for h in hilos: h.start()
    for h in hilos: h.join()
    print(f"Saldo seguro final: ${saldo_seguro}")


if __name__ == "__main__":
    main()
