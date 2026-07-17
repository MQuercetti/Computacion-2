#!/usr/bin/env python3
"""
banco_race.py - Ejercicio de síntesis de mmap.

Banco con cuentas en memoria compartida (multiprocessing.Array).
Múltiples cajeros (procesos) transfieren dinero entre cuentas.
NO usa sincronización, así que vas a ver race conditions.

Ejecutalo varias veces: el total puede cambiar de $5000.

Prerequisito: solo Linux/macOS/Windows.
"""
import random
from multiprocessing import Array, Process


NUM_CUENTAS = 5
SALDO_INICIAL = 1000
NUM_PROCESOS = 3
TRANSFERENCIAS_POR_PROCESO = 100


def mostrar_saldos(cuentas, etiqueta):
    saldos = [cuentas[i] for i in range(NUM_CUENTAS)]
    total = sum(saldos)
    print(f"[{etiqueta}] Saldos: {saldos} | Total: {total}", flush=True)


def cajero(cuentas, cajero_id, num_transferencias):
    for _ in range(num_transferencias):
        origen = random.randint(0, NUM_CUENTAS - 1)
        destino = random.randint(0, NUM_CUENTAS - 1)
        while destino == origen:
            destino = random.randint(0, NUM_CUENTAS - 1)
        monto = random.randint(1, 50)

        if cuentas[origen] >= monto:
            # ¡No atómico!
            cuentas[origen] -= monto
            cuentas[destino] += monto

    print(f"[Cajero {cajero_id}] Completó {num_transferencias} transferencias", flush=True)


def main():
    cuentas = Array('i', [SALDO_INICIAL] * NUM_CUENTAS)

    print(f"=== Banco con {NUM_CUENTAS} cuentas ===", flush=True)
    print(f"=== Saldo total esperado: {NUM_CUENTAS * SALDO_INICIAL} ===\n", flush=True)

    mostrar_saldos(cuentas, "INICIO")

    procesos = [
        Process(target=cajero, args=(cuentas, i, TRANSFERENCIAS_POR_PROCESO))
        for i in range(NUM_PROCESOS)
    ]
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()

    mostrar_saldos(cuentas, "FINAL")

    total_final = sum(cuentas[i] for i in range(NUM_CUENTAS))
    total_esperado = NUM_CUENTAS * SALDO_INICIAL

    if total_final != total_esperado:
        print(f"\n¡ERROR! Se perdieron ${total_esperado - total_final}", flush=True)
        print("Esto es una race condition - se necesita sincronización", flush=True)
    else:
        print("\nTodo correcto (pero fue suerte - ejecutalo varias veces)", flush=True)


if __name__ == "__main__":
    main()
