"""
Script de benchmarks y mediciones obligatorias para el TP2.

Ejecuta y registra las tres mediciones requeridas por la consigna:
1. Concurrencia I/O: 20 descargas secuenciales vs 20 concurrentes + speedup.
2. Event loop bloqueado: latencia de GET /tareas con y sin run_in_executor para CPU-bound.
3. Techo del pool: aumento progresivo de concurrencia y análisis de saturación.
"""

import asyncio
import hashlib
import time
from typing import List, Tuple
import httpx

from src.tasks.cpu_bound import compute_iterative_hash
from src.tasks.io_bound import ejecutar_descargas


async def medir_io_secuencial_vs_concurrente() -> Tuple[float, float, float]:
    """Medición 1: 20 descargas secuenciales vs 20 concurrentes."""
    print("\n--- Medición 1: Concurrencia I/O (20 descargas) ---")
    # Usamos URLs rápidas y confiables de prueba (o endpoints públicos)
    urls = [
        f"https://httpbin.org/status/200?i={i}" for i in range(20)
    ]

    # Secuencial
    async with httpx.AsyncClient() as client:
        inicio_sec = time.perf_counter()
        for u in urls:
            try:
                await client.get(u, timeout=10.0)
            except Exception:
                pass
        tiempo_secuencial = time.perf_counter() - inicio_sec

    # Concurrente (asyncio.gather)
    inicio_conc = time.perf_counter()
    await ejecutar_descargas(urls)
    tiempo_concurrente = time.perf_counter() - inicio_conc

    speedup = tiempo_secuencial / tiempo_concurrente if tiempo_concurrente > 0 else 1.0
    print(f"Secuencial:  {tiempo_secuencial:.3f} s")
    print(f"Concurrente: {tiempo_concurrente:.3f} s")
    print(f"Speedup:     {speedup:.2f}x")
    return tiempo_secuencial, tiempo_concurrente, speedup


async def medir_event_loop_bloqueado() -> Tuple[float, float]:
    """Medición 2: impacto de CPU-bound en el event loop con y sin ProcessPoolExecutor."""
    print("\n--- Medición 2: Event Loop bloqueado por CPU-bound ---")
    from concurrent.futures import ProcessPoolExecutor

    iteraciones = 1_500_000
    texto = "medicion_bloqueo_event_loop"
    loop = asyncio.get_running_loop()

    # CASO A: Tarea CPU-bound directa en la corrutina (sin executor)
    # Lanzamos una corrutina que intente medir el retraso cada 5ms
    retrasos_bloqueado = []
    detener_ping = False

    async def medir_retraso_loop():
        while not detener_ping:
            t0 = time.perf_counter()
            await asyncio.sleep(0.005)
            dt = time.perf_counter() - t0
            retrasos_bloqueado.append(dt)

    ping_task = asyncio.create_task(medir_retraso_loop())
    await asyncio.sleep(0.01)  # Asegurar que arrancó

    # Ejecutamos el cómputo pesado DIRECTAMENTE en el event loop bloqueándolo
    t_inicio_bloqueo = time.perf_counter()
    compute_iterative_hash(texto, iteraciones)
    duracion_computo = time.perf_counter() - t_inicio_bloqueo

    detener_ping = True
    await ping_task

    max_latencia_bloqueado = max(retrasos_bloqueado) if retrasos_bloqueado else duracion_computo

    # CASO B: Con ProcessPoolExecutor
    retrasos_no_bloqueado = []
    detener_ping_2 = False

    async def medir_retraso_loop_2():
        while not detener_ping_2:
            t0 = time.perf_counter()
            await asyncio.sleep(0.005)
            dt = time.perf_counter() - t0
            retrasos_no_bloqueado.append(dt)

    ping_task_2 = asyncio.create_task(medir_retraso_loop_2())
    await asyncio.sleep(0.01)

    with ProcessPoolExecutor(max_workers=2) as pool:
        await loop.run_in_executor(pool, compute_iterative_hash, texto, iteraciones)

    detener_ping_2 = True
    await ping_task_2

    max_latencia_no_bloqueado = max(retrasos_no_bloqueado) if retrasos_no_bloqueado else 0.005

    print(f"Duración cómputo CPU: {duracion_computo:.4f} s")
    print(f"Max latencia event loop SIN executor (bloqueado): {max_latencia_bloqueado:.4f} s")
    print(f"Max latencia event loop CON executor (desacoplado): {max_latencia_no_bloqueado:.4f} s")
    return max_latencia_bloqueado, max_latencia_no_bloqueado


async def medir_techo_pool():
    """Medición 3: escalado de tareas en el pool."""
    print("\n--- Medición 3: Techo del pool de workers ---")
    from src.task_manager import TaskManager
    from src.models import CrearTareaRequest, TipoTarea

    # Creamos un manager de 4 workers
    manager = TaskManager(worker_count=4)
    await manager.start()

    cargas = [10, 20, 50, 100]
    resultados = []

    for n in cargas:
        inicio = time.perf_counter()
        reqs = [
            CrearTareaRequest(tipo=TipoTarea.ESPERAR, segundos=0.1)
            for _ in range(n)
        ]
        respuestas = [await manager.encolar_tarea(r) for r in reqs]
        
        # Esperar a que todas completen
        ids = [r.id for r in respuestas]
        while True:
            pendientes = [
                manager.obtener_tarea(tid)
                for tid in ids
            ]
            if all(t.estado.value in ["completada", "fallida"] for t in pendientes):
                break
            await asyncio.sleep(0.05)

        total_tiempo = time.perf_counter() - inicio
        throughput = n / total_tiempo
        print(f"N={n:3d} tareas de 0.1s | Tiempo total: {total_tiempo:.3f}s | Throughput: {throughput:.1f} tareas/s")
        resultados.append((n, total_tiempo, throughput))

    await manager.stop()
    return resultados


async def main():
    print("=== INICIANDO MEDICIONES OBLIGATORIAS TP2 ===")
    await medir_io_secuencial_vs_concurrente()
    await medir_event_loop_bloqueado()
    await medir_techo_pool()
    print("\n=== MEDICIONES FINALIZADAS CON ÉXITO ===")


if __name__ == "__main__":
    asyncio.run(main())
