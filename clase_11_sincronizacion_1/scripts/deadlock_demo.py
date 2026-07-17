#!/usr/bin/env python3
"""
deadlock_demo.py - Ejercicio 6 de Sincronización avanzada.

Demuestra un deadlock: dos hilos toman locks en orden inverso.
Después muestra cómo prevenirlo imponiendo un orden global de adquisición.
"""
import threading
import time


def demostrar_deadlock():
    lock_a = threading.Lock()
    lock_b = threading.Lock()

    def thread_1():
        with lock_a:
            print("Thread 1: tiene A", flush=True)
            time.sleep(0.1)
            with lock_b:
                print("Thread 1: tiene A y B", flush=True)

    def thread_2():
        with lock_b:
            print("Thread 2: tiene B", flush=True)
            time.sleep(0.1)
            with lock_a:
                print("Thread 2: tiene B y A", flush=True)

    t1 = threading.Thread(target=thread_1)
    t2 = threading.Thread(target=thread_2)
    t1.start(); t2.start()

    t1.join(timeout=2)
    t2.join(timeout=2)

    if t1.is_alive() or t2.is_alive():
        print("¡DEADLOCK DETECTADO!", flush=True)
        return False
    return True


def version_corregida():
    lock_a = threading.Lock()
    lock_b = threading.Lock()

    def thread_ordenado(nombre):
        with lock_a:  # Siempre A primero
            print(f"{nombre}: tiene A", flush=True)
            with lock_b:  # Luego B
                print(f"{nombre}: tiene A y B", flush=True)
                time.sleep(0.1)

    t1 = threading.Thread(target=thread_ordenado, args=("Thread 1",))
    t2 = threading.Thread(target=thread_ordenado, args=("Thread 2",))
    t1.start(); t2.start()
    t1.join(); t2.join()

    print("¡Completado sin deadlock!", flush=True)


def main():
    print("=== Versión con deadlock ===", flush=True)
    demostrar_deadlock()

    print("\n=== Versión corregida ===", flush=True)
    version_corregida()


if __name__ == "__main__":
    main()
