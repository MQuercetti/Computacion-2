#!/usr/bin/env python3
"""
threading_local.py - Ejercicio 8 de Threading.

threading.local() para aislar estado entre hilos. Cada thread
atiende un "request" con su propio usuario, ip, timestamp.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import random
import threading
import time


contexto = threading.local()


def get_contexto():
    return {
        "usuario": getattr(contexto, "usuario", None),
        "ip": getattr(contexto, "ip", None),
        "timestamp": getattr(contexto, "timestamp", None),
    }


def atender_request(request_id):
    contexto.usuario = f"user_{random.randint(1000, 9999)}"
    contexto.ip = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
    contexto.timestamp = time.time()

    print(f"Request {request_id} iniciando | contexto: {get_contexto()}", flush=True)
    time.sleep(random.uniform(0.1, 0.5))
    print(f"Request {request_id} finalizando | usuario: {contexto.usuario}", flush=True)


def main():
    hilos = [
        threading.Thread(target=atender_request, args=(i,), name=f"Request-{i}")
        for i in range(6)
    ]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    print("\nTodos los requests atendidos")


if __name__ == "__main__":
    main()
