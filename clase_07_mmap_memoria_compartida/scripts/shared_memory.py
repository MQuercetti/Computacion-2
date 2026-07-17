#!/usr/bin/env python3
"""
shared_memory.py - Ejercicio 6.1 de mmap.

Compartir datos entre procesos con multiprocessing.shared_memory.
Un productor escribe 10 valores, un consumidor los lee.

Prerequisito: solo Linux/macOS/Windows (>= 3.8).
"""
import struct
from multiprocessing import Process, shared_memory


def productor(shm_name, num_valores):
    shm = shared_memory.SharedMemory(name=shm_name)
    for i in range(num_valores):
        struct.pack_into('i', shm.buf, i * 4, i * i)
    shm.buf[-1] = 1  # marcar como listo
    print(f"[PRODUCTOR] Escribí {num_valores} valores", flush=True)
    shm.close()


def consumidor(shm_name, num_valores):
    import time
    shm = shared_memory.SharedMemory(name=shm_name)
    while shm.buf[-1] != 1:
        time.sleep(0.01)
    valores = [
        struct.unpack_from('i', shm.buf, i * 4)[0]
        for i in range(num_valores)
    ]
    print(f"[CONSUMIDOR] Leí: {valores}", flush=True)
    shm.close()


def main():
    NUM = 10
    shm = shared_memory.SharedMemory(create=True, size=NUM * 4 + 1)

    p_prod = Process(target=productor, args=(shm.name, NUM))
    p_cons = Process(target=consumidor, args=(shm.name, NUM))

    p_cons.start()
    p_prod.start()
    p_prod.join()
    p_cons.join()

    shm.close()
    shm.unlink()


if __name__ == "__main__":
    main()
