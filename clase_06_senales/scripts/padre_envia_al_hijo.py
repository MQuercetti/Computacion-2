#!/usr/bin/env python3
"""
padre_envia_al_hijo.py - Ejercicio 3.1 de Señales.

El padre envía señales al hijo vía os.kill(). El hijo las maneja:
- SIGUSR1: incrementa un contador
- SIGUSR2: muestra el contador

Prerequisito: solo Linux/macOS (os.fork).
"""
import os
import signal
import time


def main():
    pid = os.fork()

    if pid == 0:
        # === HIJO ===
        estado = {"contador": 0}

        def incrementar(sig, frame):
            estado["contador"] += 1
            print(f"[HIJO] Contador incrementado: {estado['contador']}", flush=True)

        def mostrar(sig, frame):
            print(f"[HIJO] Valor actual: {estado['contador']}", flush=True)

        signal.signal(signal.SIGUSR1, incrementar)
        signal.signal(signal.SIGUSR2, mostrar)

        print(f"[HIJO] PID={os.getpid()}, esperando señales...", flush=True)
        while True:
            signal.pause()  # Esperar señales

    else:
        # === PADRE ===
        time.sleep(0.5)  # Dar tiempo al hijo

        print("[PADRE] Enviando SIGUSR1 (incrementar) x3", flush=True)
        for _ in range(3):
            os.kill(pid, signal.SIGUSR1)
            time.sleep(0.3)

        print("[PADRE] Enviando SIGUSR2 (mostrar)", flush=True)
        os.kill(pid, signal.SIGUSR2)
        time.sleep(0.3)

        print("[PADRE] Enviando SIGUSR1 x2", flush=True)
        for _ in range(2):
            os.kill(pid, signal.SIGUSR1)
            time.sleep(0.3)

        print("[PADRE] Enviando SIGUSR2 (mostrar)", flush=True)
        os.kill(pid, signal.SIGUSR2)
        time.sleep(0.3)

        print("[PADRE] Terminando hijo", flush=True)
        os.kill(pid, signal.SIGTERM)
        os.wait()


if __name__ == "__main__":
    main()
