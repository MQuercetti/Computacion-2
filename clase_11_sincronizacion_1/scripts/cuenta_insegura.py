#!/usr/bin/env python3
"""
cuenta_insegura.py - Ejercicio 1.1 de Sincronización avanzada.

Cuenta bancaria con race condition. 10 hilos hacen operaciones
aleatorias (depositar o retirar $10). El saldo final es impredecible
por la falta de lock.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import random
import threading
import time


class CuentaInsegura:
    def __init__(self, saldo):
        self.saldo = saldo

    def depositar(self, cantidad):
        actual = self.saldo
        time.sleep(0.001)
        self.saldo = actual + cantidad

    def retirar(self, cantidad):
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
    cuenta = CuentaInsegura(1000)
    threads = [threading.Thread(target=operaciones_aleatorias, args=(cuenta,)) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Saldo esperado: 1000 (si no hay errores)")
    print(f"Saldo obtenido: {cuenta.saldo}")


if __name__ == "__main__":
    main()
