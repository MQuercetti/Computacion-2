#!/usr/bin/env python3
"""
read_write_lock.py - Ejercicio 5 (OBLIGATORIO) de Sincronización avanzada.

Implementación de un Readers-Writers Lock. Múltiples lectores pueden
leer a la vez, pero un escritor tiene acceso exclusivo.

Reglas:
- Múltiples lectores pueden leer simultáneamente
- Solo un escritor puede escribir a la vez
- Mientras hay escritor, no pueden haber lectores
- Mientras hay lectores, no pueden haber escritores

Prerequisito: funciona en Linux/macOS/Windows.
"""
import random
import threading
import time


class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.writers = 0
        self.lock = threading.Lock()
        self.can_read = threading.Condition(self.lock)
        self.can_write = threading.Condition(self.lock)

    def acquire_read(self):
        with self.lock:
            while self.writers > 0:
                self.can_read.wait()
            self.readers += 1

    def release_read(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0:
                self.can_write.notify()

    def acquire_write(self):
        with self.lock:
            while self.readers > 0 or self.writers > 0:
                self.can_write.wait()
            self.writers += 1

    def release_write(self):
        with self.lock:
            self.writers -= 1
            self.can_read.notify_all()
            self.can_write.notify()


class ReadLock:
    def __init__(self, rwlock):
        self.rwlock = rwlock

    def __enter__(self):
        self.rwlock.acquire_read()

    def __exit__(self, *args):
        self.rwlock.release_read()


class WriteLock:
    def __init__(self, rwlock):
        self.rwlock = rwlock

    def __enter__(self):
        self.rwlock.acquire_write()

    def __exit__(self, *args):
        self.rwlock.release_write()


def main():
    rwlock = ReadWriteLock()
    datos = {"valor": 0, "lecturas": 0, "escrituras": 0}

    def lector(id):
        for _ in range(5):
            with ReadLock(rwlock):
                valor = datos["valor"]
                datos["lecturas"] += 1
                print(f"[Lector {id}] Leyó valor={valor}", flush=True)
                time.sleep(random.uniform(0.05, 0.15))
            time.sleep(random.uniform(0.1, 0.2))

    def escritor(id):
        for i in range(3):
            with WriteLock(rwlock):
                datos["valor"] = id * 100 + i
                datos["escrituras"] += 1
                print(f"[Escritor {id}] Escribió valor={datos['valor']}", flush=True)
                time.sleep(random.uniform(0.1, 0.2))
            time.sleep(random.uniform(0.2, 0.4))

    threads = [threading.Thread(target=lector, args=(i,)) for i in range(5)]
    threads += [threading.Thread(target=escritor, args=(i,)) for i in range(2)]
    random.shuffle(threads)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\nEstadísticas finales:", flush=True)
    print(f"  Valor final: {datos['valor']}", flush=True)
    print(f"  Total lecturas: {datos['lecturas']}", flush=True)
    print(f"  Total escrituras: {datos['escrituras']}", flush=True)


if __name__ == "__main__":
    main()
