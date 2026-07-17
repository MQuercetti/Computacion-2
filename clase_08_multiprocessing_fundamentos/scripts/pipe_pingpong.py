#!/usr/bin/env python3
"""
pipe_pingpong.py - Ejercicio 4 de Multiprocessing fundamentos.

Padre e hijo se mandan 5 mensajes alternados (ping-pong) usando
multiprocessing.Pipe().

Prerequisito: funciona en Linux/macOS/Windows.
"""
from multiprocessing import Pipe, Process


def hijo(conn):
    """Recibe 'ping', responde 'pong'."""
    for i in range(5):
        msg = conn.recv()
        print(f"[HIJO] recibí: {msg}", flush=True)
        conn.send(f"pong-{i}")
    conn.close()


def main():
    parent_conn, child_conn = Pipe()
    p = Process(target=hijo, args=(child_conn,))
    p.start()

    for i in range(5):
        parent_conn.send(f"ping-{i}")
        print(f"[PADRE] mandé: ping-{i}", flush=True)
        respuesta = parent_conn.recv()
        print(f"[PADRE] recibí: {respuesta}", flush=True)

    p.join()
    parent_conn.close()
    print("Fin")


if __name__ == "__main__":
    main()
