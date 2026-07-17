#!/usr/bin/env python3
"""
barrier_fases.py - Ejercicio 3 de Sincronización avanzada.

Procesamiento por fases con threading.Barrier. 4 workers hacen
fase 1, esperan en la barrier, hacen fase 2, esperan de nuevo.
La barrier tiene una acción que imprime el estado después de cada fase.
"""
import random
import threading
import time


NUM_WORKERS = 4
datos = [0] * NUM_WORKERS
resultados_fase1 = [0] * NUM_WORKERS
resultados_fase2 = [0] * NUM_WORKERS


def imprimir_estado():
    print(f"  Resultados fase 1: {resultados_fase1}", flush=True)
    print(f"  Resultados fase 2: {resultados_fase2}", flush=True)


barrera = threading.Barrier(NUM_WORKERS, action=imprimir_estado)


def worker(id):
    print(f"[Worker {id}] Fase 1: procesando...", flush=True)
    time.sleep(random.uniform(0.5, 1.5))
    resultados_fase1[id] = datos[id] * 2
    print(f"[Worker {id}] Fase 1: completada", flush=True)

    barrera.wait()

    print(f"[Worker {id}] Fase 2: combinando...", flush=True)
    time.sleep(random.uniform(0.3, 0.8))
    vecino = (id + 1) % NUM_WORKERS
    resultados_fase2[id] = resultados_fase1[id] + resultados_fase1[vecino]
    print(f"[Worker {id}] Fase 2: completada", flush=True)

    barrera.wait()
    print(f"[Worker {id}] Procesamiento completo!", flush=True)


def main():
    global datos
    datos = [i * 10 for i in range(NUM_WORKERS)]
    print(f"Datos iniciales: {datos}\n", flush=True)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(NUM_WORKERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\nResultados finales: {resultados_fase2}")


if __name__ == "__main__":
    main()
