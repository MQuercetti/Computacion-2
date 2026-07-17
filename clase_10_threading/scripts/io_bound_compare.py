#!/usr/bin/env python3
"""
io_bound_compare.py - Ejercicio 2 de Threading.

Compara tiempo de "descargas" simuladas: secuencial vs threading.
Como las descargas son I/O-bound (time.sleep), threading gana.

Prerequisito: funciona en Linux/macOS/Windows.
"""
import threading
import time


URLS = [f"http://servidor.com/archivo_{i}.zip" for i in range(5)]
DEMORA = 1  # segundos por descarga


def simular_descarga(url, demora):
    time.sleep(demora)
    print(f"Descargado: {url}", flush=True)


def main():
    # Secuencial
    inicio = time.perf_counter()
    for url in URLS:
        simular_descarga(url, DEMORA)
    t_secuencial = time.perf_counter() - inicio
    print(f"\nSecuencial: {t_secuencial:.2f}s")

    # Paralelo con threading
    inicio = time.perf_counter()
    hilos = [
        threading.Thread(target=simular_descarga, args=(url, DEMORA))
        for url in URLS
    ]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    t_paralelo = time.perf_counter() - inicio
    print(f"Threading:  {t_paralelo:.2f}s")
    print(f"Mejora:     {t_secuencial / t_paralelo:.1f}x")


if __name__ == "__main__":
    main()
