"""
recolector.py — enumera /proc y publica los PIDs por una Queue.

Es el ÚNICO proceso que tiene la lista "maestra" de qué PIDs existen.
Los analizadores consumen de la Queue y leen /proc/<pid>/ por su cuenta.

¿Por qué Queue y no Manager.list?
    - Queue está optimizada para productor-consumidor (es lo que vimos en
      clase 8: productor_consumidor.py).
    - Manager.list también funcionaría pero es más lento y la sincronización
      es más frágil.
"""

import os
import time
from multiprocessing import Queue


def recolector_loop(queue_pids: Queue, intervalo: float = 1.0):
    """Loop principal del recolector.

    Cada `intervalo` segundos:
        1. Lista los PIDs en /proc
        2. Los pone en la queue (sobrescribiendo el lote anterior — el más
           reciente es el que importa)
        3. Si la queue tiene más de 1 lote acumulado, drena los viejos.

    Esto es un patrón "latest-only": al consumidor le importa solo el último
    snapshot de PIDs, no la historia.
    """
    while True:
        try:
            pids = []
            for nombre in os.listdir("/proc"):
                if nombre.isdigit():
                    pids.append(int(nombre))
        except FileNotFoundError:
            pids = []

        # Drenar la queue primero para que el consumidor no se atrase.
        while not queue_pids.empty():
            try:
                queue_pids.get_nowait()
            except Exception:
                break
        queue_pids.put(pids)

        time.sleep(intervalo)


if __name__ == "__main__":
    # Mini-prueba: crear una queue y mostrar qué se publica.
    q = Queue()
    recolector_loop(q, intervalo=0)
    print(f"Lote publicado: {q.get()[:10]}... ({q.qsize()} elementos)")
