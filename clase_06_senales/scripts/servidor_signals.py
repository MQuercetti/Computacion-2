#!/usr/bin/env python3
"""
servidor_signals.py - Ejercicio 5 (OBLIGATORIO) de Señales.

Servidor que responde a múltiples señales:
- SIGTERM/SIGINT: shutdown limpio
- SIGHUP: recargar configuración
- SIGUSR1: mostrar estadísticas
- SIGUSR2: rotar logs (simulado)

Uso:
    python servidor_signals.py        # en una terminal
    kill -HUP <pid>                   # en otra: recargar config
    kill -USR1 <pid>                  # mostrar stats
    kill -USR2 <pid>                  # rotar logs
    kill <pid>                        # shutdown limpio
"""
import os
import signal
import time


class Servidor:
    def __init__(self):
        self.ejecutando = True
        self.config = {"max_conexiones": 100, "timeout": 30}
        self.stats = {"requests": 0, "errores": 0, "inicio": time.time()}
        self._registrar_manejadores()

    def _registrar_manejadores(self):
        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGHUP, self._reload_config)
        signal.signal(signal.SIGUSR1, self._mostrar_stats)
        signal.signal(signal.SIGUSR2, self._rotar_logs)

    def _shutdown(self, sig, frame):
        nombre = signal.Signals(sig).name
        print(f"\n[{nombre}] Iniciando shutdown...", flush=True)
        self.ejecutando = False

    def _reload_config(self, sig, frame):
        print("\n[SIGHUP] Recargando configuración...", flush=True)
        self.config["max_conexiones"] += 10
        self.config["recargado"] = time.ctime()
        print(f"[SIGHUP] Nueva config: {self.config}", flush=True)

    def _mostrar_stats(self, sig, frame):
        uptime = time.time() - self.stats["inicio"]
        print(f"\n[SIGUSR1] === Estadísticas ===", flush=True)
        print(f"  Uptime: {uptime:.1f}s", flush=True)
        print(f"  Requests: {self.stats['requests']}", flush=True)
        print(f"  Errores: {self.stats['errores']}", flush=True)
        print(f"  Config: {self.config}", flush=True)

    def _rotar_logs(self, sig, frame):
        print(f"\n[SIGUSR2] Rotando logs...", flush=True)
        print(f"[SIGUSR2] Logs rotados a server.log.{int(time.time())}", flush=True)

    def procesar_request(self):
        """Simula procesamiento de una request."""
        self.stats["requests"] += 1
        time.sleep(0.1)
        if self.stats["requests"] % 10 == 0:
            self.stats["errores"] += 1

    def run(self):
        print(f"Servidor iniciado (PID {os.getpid()})", flush=True)
        print("Comandos disponibles:", flush=True)
        print(f"  kill -HUP {os.getpid()}   -> Recargar config", flush=True)
        print(f"  kill -USR1 {os.getpid()}  -> Ver stats", flush=True)
        print(f"  kill -USR2 {os.getpid()}  -> Rotar logs", flush=True)
        print(f"  kill {os.getpid()}        -> Shutdown", flush=True)
        print(flush=True)

        while self.ejecutando:
            self.procesar_request()

        print("Realizando cleanup...", flush=True)
        time.sleep(0.5)
        print(f"Servidor terminado. Requests procesadas: {self.stats['requests']}", flush=True)


def main():
    Servidor().run()


if __name__ == "__main__":
    main()
