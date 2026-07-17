#!/usr/bin/env python3
"""
pool_supervisado.py - Ejercicio 6 de Señales.

Supervisor que mantiene un pool de N workers. Si un worker muere
inesperadamente, el supervisor lo reemplaza. Usa SIGCHLD para
detectar cuándo un worker termina.

Prerequisito: solo Linux/macOS.
"""
import os
import random
import signal
import time


class WorkerPool:
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.workers = {}  # pid -> info
        self.ejecutando = True
        self._next_id = 0

        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGCHLD, self._sigchld)

    def _shutdown(self, sig, frame):
        print("\n[SUPERVISOR] Shutdown solicitado", flush=True)
        self.ejecutando = False
        for pid in list(self.workers.keys()):
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

    def _sigchld(self, sig, frame):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    break
                if pid in self.workers:
                    info = self.workers.pop(pid)
                    codigo = os.WEXITSTATUS(status) if os.WIFEXITED(status) else -1
                    print(f"[SUPERVISOR] Worker {info['id']} (pid {pid}) terminó con código {codigo}", flush=True)
            except ChildProcessError:
                break

    def _worker_main(self, worker_id):
        print(f"[Worker {worker_id}] Iniciado (PID {os.getpid()})", flush=True)

        def worker_shutdown(sig, frame):
            print(f"[Worker {worker_id}] Recibí SIGTERM, terminando...", flush=True)
            os._exit(0)

        signal.signal(signal.SIGTERM, worker_shutdown)

        for i in range(random.randint(5, 15)):
            print(f"[Worker {worker_id}] Trabajando... ({i})", flush=True)
            time.sleep(0.5)

        if random.random() < 0.3:
            print(f"[Worker {worker_id}] ¡Error simulado!", flush=True)
            os._exit(1)

        print(f"[Worker {worker_id}] Trabajo completado", flush=True)
        os._exit(0)

    def spawn_worker(self):
        worker_id = self._next_id
        self._next_id += 1
        pid = os.fork()
        if pid == 0:
            self._worker_main(worker_id)
        else:
            self.workers[pid] = {"id": worker_id, "started": time.time()}
            print(f"[SUPERVISOR] Spawneó worker {worker_id} (PID {pid})", flush=True)

    def run(self):
        print(f"[SUPERVISOR] PID {os.getpid()}, iniciando {self.num_workers} workers", flush=True)
        for _ in range(self.num_workers):
            self.spawn_worker()

        while self.ejecutando:
            time.sleep(1)
            if len(self.workers) < self.num_workers and self.ejecutando:
                print(f"[SUPERVISOR] Solo {len(self.workers)} workers activos, spawneando más", flush=True)
                self.spawn_worker()

        while self.workers:
            time.sleep(0.1)

        print("[SUPERVISOR] Todos los workers terminados", flush=True)


def main():
    WorkerPool(3).run()


if __name__ == "__main__":
    main()
