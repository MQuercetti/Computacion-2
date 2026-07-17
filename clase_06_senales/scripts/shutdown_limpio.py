#!/usr/bin/env python3
"""
shutdown_limpio.py - Ejercicio 2.2 de Señales.

Demuestra shutdown limpio con SIGTERM/SIGINT. Simula adquisición
y liberación de recursos: si recibe la señal a mitad de trabajo,
libera todo antes de salir.

Probalo: en otra terminal, `kill <pid>` o Ctrl+C.
"""
import os
import signal
import time


class Aplicacion:
    def __init__(self):
        self.ejecutando = True
        self.recursos = []
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown(self, sig, frame):
        nombre = signal.Signals(sig).name
        print(f"\nRecibí {nombre}, cerrando...", flush=True)
        self.ejecutando = False

    def adquirir_recurso(self, nombre):
        print(f"Adquiriendo recurso: {nombre}", flush=True)
        self.recursos.append(nombre)

    def liberar_recursos(self):
        for recurso in reversed(self.recursos):
            print(f"Liberando recurso: {recurso}", flush=True)
            time.sleep(0.3)
        self.recursos.clear()

    def run(self):
        print(f"PID: {os.getpid()}")
        print("Enviá 'kill <pid>' o Ctrl+C para terminar limpiamente")

        self.adquirir_recurso("base_de_datos")
        self.adquirir_recurso("archivo_log")
        self.adquirir_recurso("conexion_red")

        while self.ejecutando:
            print("Trabajando...", flush=True)
            time.sleep(1)

        self.liberar_recursos()
        print("Aplicación terminada correctamente")


def main():
    Aplicacion().run()


if __name__ == "__main__":
    main()
