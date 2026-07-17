#!/usr/bin/env python3
"""
zombie_demo.py - Ejercicio 4 de Procesos - fork, exec, wait.

Crea un zombie (proceso terminado cuyo padre no llama a wait()).
Para verlo, en otra terminal corré:

    ps aux | grep -E 'Z|defunct'

El padre vive 30 segundos. Si descomentás el os.wait() dentro del
padre, el zombie desaparece.

Prerequisito: solo Linux/macOS.
"""
import os
import time


def main():
    pid = os.fork()
    if pid == 0:
        # Hijo: termina inmediatamente
        print(f"[Hijo PID={os.getpid()}] termino inmediatamente")
        os._exit(0)
    else:
        # Padre: NO espera al hijo -> zombie
        print(f"[Padre PID={os.getpid()}] creé hijo {pid}, no lo voy a esperar")
        print("Mirá con: ps aux | grep -E 'Z|defunct'")
        time.sleep(30)
        # Para limpiar: descomentar
        # os.wait()
        # print("Hijo recogido, ya no es zombie")


if __name__ == "__main__":
    main()
