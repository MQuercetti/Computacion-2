#!/usr/bin/env python3
"""
productor_consumidor.py - Ejercicio 7 de Threading.

Sistema productor-consumidor con queue.Queue. 4 workers procesan
20 imágenes desde una cola. Cada imagen tarda 0.5s.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import queue
import threading
import time


resultados = {}
resultados_lock = threading.Lock()


def procesar_imagen(nombre):
    time.sleep(0.5)
    return f"{nombre} -> procesada"


def worker(q, worker_id):
    contador = 0
    while True:
        imagen = q.get()
        if imagen is None:
            break
        resultado = procesar_imagen(imagen)
        print(f"Worker-{worker_id}: {resultado}", flush=True)
        contador += 1
        q.task_done()
    with resultados_lock:
        resultados[f"Worker-{worker_id}"] = contador


def main():
    cola = queue.Queue()

    workers = [threading.Thread(target=worker, args=(cola, i)) for i in range(4)]
    for w in workers:
        w.start()

    inicio = time.perf_counter()
    for i in range(1, 21):
        cola.put(f"imagen_{i:03d}.jpg")

    cola.join()

    for _ in workers:
        cola.put(None)
    for w in workers:
        w.join()

    tiempo = time.perf_counter() - inicio
    print(f"\nTiempo total: {tiempo:.2f}s", flush=True)
    print("\nImágenes por worker:")
    for nombre, cant in resultados.items():
        print(f"  {nombre}: {cant} imágenes")


if __name__ == "__main__":
    main()
