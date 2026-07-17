#!/usr/bin/env python3
"""
manager_dict_list.py - Ejercicio 4 de Multiprocessing avanzado.

Manager() para compartir estructuras complejas (dict, list) entre
procesos. 5 workers reportan su estado en un dict compartido y
agregan un mensaje a una lista compartida.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import random
import time
from multiprocessing import Manager, Process


def worker(shared_dict, shared_list, id):
    duracion = random.uniform(0.2, 1.0)
    time.sleep(duracion)

    shared_dict[f"worker_{id}"] = {
        "status": "done",
        "result": id ** 2,
        "duracion": round(duracion, 2),
    }
    shared_list.append(f"Worker {id} completó en {duracion:.2f}s")


def main():
    with Manager() as manager:
        d = manager.dict()
        l = manager.list()

        procs = [Process(target=worker, args=(d, l, i)) for i in range(5)]
        for p in procs:
            p.start()
        for p in procs:
            p.join()

        print("Diccionario compartido:")
        for k, v in d.items():
            print(f"  {k}: {v}")

        print("\nLista compartida (orden de finalización):")
        for item in l:
            print(f"  {item}")


if __name__ == "__main__":
    main()
