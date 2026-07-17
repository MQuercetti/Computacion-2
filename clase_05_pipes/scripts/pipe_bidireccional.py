#!/usr/bin/env python3
"""
pipe_bidireccional.py - Ejercicio 3.2 de Pipes.

Comunicación bidireccional con dos pipes: padre → hijo y hijo → padre.
El padre le pregunta al hijo el cuadrado de un número.

Prerequisito: solo Linux/macOS.
"""
import os


def main():
    # Pipe 1: padre -> hijo
    p2h_read, p2h_write = os.pipe()
    # Pipe 2: hijo -> padre
    h2p_read, h2p_write = os.pipe()

    pid = os.fork()

    if pid == 0:
        # === HIJO ===
        os.close(p2h_write)  # No escribe al pipe padre->hijo
        os.close(h2p_read)   # No lee del pipe hijo->padre

        pregunta = os.read(p2h_read, 1024).decode().strip()
        print(f"[HIJO] Recibí pregunta: {pregunta}", flush=True)

        if pregunta.isdigit():
            respuesta = str(int(pregunta) ** 2)
        else:
            respuesta = "No es un número"

        os.write(h2p_write, respuesta.encode())
        print(f"[HIJO] Envié respuesta: {respuesta}", flush=True)

        os.close(p2h_read)
        os.close(h2p_write)
        os._exit(0)

    else:
        # === PADRE ===
        os.close(p2h_read)   # No lee del pipe padre->hijo
        os.close(h2p_write)  # No escribe al pipe hijo->padre

        numero = "42"
        print(f"[PADRE] Enviando número: {numero}", flush=True)
        os.write(p2h_write, numero.encode())
        os.close(p2h_write)  # Señalar que terminamos de escribir

        respuesta = os.read(h2p_read, 1024).decode()
        print(f"[PADRE] Respuesta: {numero}² = {respuesta}", flush=True)

        os.close(h2p_read)
        os.wait()


if __name__ == "__main__":
    main()
