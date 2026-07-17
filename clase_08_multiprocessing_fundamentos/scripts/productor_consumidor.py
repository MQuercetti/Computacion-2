#!/usr/bin/env python3
"""
productor_consumidor.py - Ejercicio 3 de Multiprocessing fundamentos.

Productor genera 10 items, los pone en una Queue. Consumidor los
procesa. El proceso principal coordina.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import time
from multiprocessing import Process, Queue


def productor(q, n):
    for i in range(n):
        item = f"item-{i}"
        q.put(item)
        print(f"[PRODUCTOR] puso {item}", flush=True)
        time.sleep(0.2)
    q.put(None)  # señal de fin


def consumidor(q):
    while True:
        item = q.get()
        if item is None:
            print("[CONSUMIDOR] terminó", flush=True)
            break
        print(f"[CONSUMIDOR] procesó {item}", flush=True)
        time.sleep(0.3)


def main():
    q = Queue()
    p_prod = Process(target=productor, args=(q, 10))
    p_cons = Process(target=consumidor, args=(q,))

    p_cons.start()
    p_prod.start()

    p_prod.join()
    p_cons.join()
    print("Fin")


if __name__ == "__main__":
    main()
