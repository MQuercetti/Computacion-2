#!/usr/bin/env python3
"""
cuenta_segura.py - Ejercicio 1.2 de Sincronización avanzada.

Misma cuenta que cuenta_insegura.py pero con threading.Lock. El
saldo final siempre es 1000.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import random
import threading
import time


class CuentaSegura:
    def __init__(self, saldo):
        self.saldo = saldo
        self.lock = threading.Lock()

    def depositar(self, cantidad):
        with self.lock:
            actual = self.saldo
            time.sleep(0.001)
            self.saldo = actual + cantidad

    def retirar(self, cantidad):
        with self.lock:
            actual = self.saldo
            time.sleep(0.001)
            if actual >= cantidad:
                self.saldo = actual - cantidad
                return True
            return False


def operaciones_aleatorias(cuenta):
    for _ in range(100):
        if random.choice([True, False]):
            cuenta.depositar(10)
        else:
            cuenta.retirar(10)


def main():
    cuenta = CuentaSegura(1000)
    threads = [threading.Thread(target=operaciones_aleatorias, args=(cuenta,)) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Saldo esperado: 1000")
    print(f"Saldo obtenido: {cuenta.saldo}")


if __name__ == "__main__":
    main()
