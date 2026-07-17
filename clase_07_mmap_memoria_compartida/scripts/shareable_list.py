#!/usr/bin/env python3
"""
shareable_list.py - Ejercicio 6.2 de mmap.

ShareableList: una lista de tipos básicos (int, float, str, bool)
compartida entre procesos. El tipo y tamaño máximo de cada elemento
se fija en la creación.

Prerequisito: solo Linux/macOS/Windows (>= 3.8).
"""
from multiprocessing import Process, shared_memory


def actualizar_datos(nombre_shm):
    sl = shared_memory.ShareableList(name=nombre_shm)
    sl[0] = 42
    sl[1] = 3.14159
    sl[2] = "actualizado"
    sl[3] = False
    print(f"[WORKER] Lista actualizada: {list(sl)}", flush=True)
    sl.shm.close()


def main():
    # Espacios para reservar lugar para el string
    sl = shared_memory.ShareableList(
        [0, 0.0, "          ", True],
        name="mi_lista_comp",
    )
    print(f"Antes:   {list(sl)}")

    p = Process(target=actualizar_datos, args=(sl.shm.name,))
    p.start()
    p.join()

    print(f"Después: {list(sl)}")

    sl.shm.close()
    sl.shm.unlink()


if __name__ == "__main__":
    main()
