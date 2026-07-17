#!/usr/bin/env python3
"""
pipe_padre_hijo.py - Ejercicio 3.1 de Pipes.

Comunicación básica por pipe entre padre e hijo usando os.fork() y os.pipe().
El hijo escribe 4 mensajes y el padre los lee.

Prerequisito: solo Linux/macOS (usa os.fork).
"""
import os
import sys


def main():
    # Crear pipe ANTES del fork
    read_fd, write_fd = os.pipe()

    pid = os.fork()

    if pid == 0:
        # === HIJO: escribe al pipe ===
        os.close(read_fd)  # El hijo no lee

        mensajes = ["Mensaje 1 del hijo", "Mensaje 2 del hijo", "Mensaje 3 del hijo", "FIN"]
        for msg in mensajes:
            os.write(write_fd, (msg + "\n").encode())
            print(f"[HIJO] Envié: {msg}", file=sys.stderr)

        os.close(write_fd)
        os._exit(0)

    else:
        # === PADRE: lee del pipe ===
        os.close(write_fd)  # El padre no escribe

        print("[PADRE] Esperando mensajes del hijo...\n", file=sys.stderr)

        buffer = b""
        while True:
            datos = os.read(read_fd, 1024)
            if not datos:  # EOF - el hijo cerró su extremo
                break
            buffer += datos

        for msg in buffer.decode().strip().split("\n"):
            print(f"[PADRE] Recibí: {msg}")

        os.close(read_fd)
        os.wait()
        print("\n[PADRE] Hijo terminó", file=sys.stderr)


if __name__ == "__main__":
    main()
