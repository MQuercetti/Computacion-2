"""
sistema.py — analizador de la vista 7.

Lee /proc/{stat,meminfo,loadavg,uptime} y agrega contadores globales:
    CPU% global (delta de jiffies entre lecturas)
    Memoria total / libre / buffers / cached / swap
    Load average (1, 5, 15 min)
    Cantidad de procesos totales, por estado, threads totales, zombies
    Top 3 por CPU y por memoria (deriva del snapshot de 'resumen'/'memoria')
"""

import os
import time
from .. import procfs
from ..agregador import escribir_slot


def analizar(pids, snapshot, intervalos, verbose):
    cpu_prev = None
    t_prev = None

    while True:
        cpu_actual = procfs.leer_stat_global()
        meminfo = procfs.leer_meminfo()
        loadavg = procfs.leer_loadavg()
        uptime = procfs.leer_uptime()
        btime = procfs.btime()

        # Calcular CPU% global a partir del delta.
        cpu_pct = _cpu_pct_global(cpu_actual, cpu_prev, t_prev)

        # Conteos por estado, threads totales, zombies — a partir de los
        # PIDs que el recolector nos pasó.
        conteo_estados = {}
        total_threads = 0
        zombies = 0
        for pid in pids:
            stat = procfs.leer_stat(pid)
            status = procfs.leer_status(pid)
            if not stat:
                continue
            estado = stat["state"]
            conteo_estados[estado] = conteo_estados.get(estado, 0) + 1
            try:
                total_threads += int(status.get("Threads", 0))
            except ValueError:
                pass
            if estado == "Z":
                zombies += 1

        datos = {
            "cpu_pct": cpu_pct,
            "cpu_campos": cpu_actual,
            "mem_total": meminfo.get("MemTotal", 0),
            "mem_free": meminfo.get("MemFree", 0),
            "mem_available": meminfo.get("MemAvailable", 0),
            "buffers": meminfo.get("Buffers", 0),
            "cached": meminfo.get("Cached", 0),
            "swap_total": meminfo.get("SwapTotal", 0),
            "swap_free": meminfo.get("SwapFree", 0),
            "loadavg": loadavg,
            "uptime": uptime,
            "btime": btime,
            "total_procesos": len(pids),
            "conteo_estados": conteo_estados,
            "total_threads": total_threads,
            "zombies": zombies,
            "top_cpu": [],     # TODO: derivar de snapshot['resumen']
            "top_mem": [],     # TODO: derivar de snapshot['memoria']
            "n_cpus": os.cpu_count() or 1,
        }

        escribir_slot(snapshot, "sistema", datos)

        # Actualizamos lo previo para el próximo cálculo de delta.
        cpu_prev = cpu_actual
        t_prev = time.time()

        time.sleep(max(0.1, intervalos["sistema"].value))


def _cpu_pct_global(actual, previo, t_prev):
    """Calcula CPU% global a partir de dos lecturas de /proc/stat.

    Fórmula: ((user+nice+system) ahora − antes) / (total ahora − antes) * 100.
    Si no hay lectura previa devuelve 0.
    """
    if not actual or not previo or t_prev is None:
        return 0.0
    busy_keys = ("user", "nice", "system", "irq", "softirq", "steal")
    busy_actual = sum(actual.get(k, 0) for k in busy_keys)
    busy_prev = sum(previo.get(k, 0) for k in busy_keys)
    total_actual = sum(actual.values())
    total_prev = sum(previo.values())

    delta_busy = busy_actual - busy_prev
    delta_total = total_actual - total_prev

    if delta_total <= 0:
        return 0.0
    return round(100.0 * delta_busy / delta_total, 2)


# TODO: para el top 3 por CPU y por memoria, en vez de volver a leer /proc,
# usá los datos que ya escribieron los analizadores de 'resumen' y 'memoria'
# en el snapshot. Hacé snapshot['resumen']['datos'] y snapshot['memoria']['datos'],
# ordenalos por cpu_pct y vm_rss respectivamente, y quedate con los 3 primeros.
#
# Ojo: el Manager.dict se accede con corchetes — el lock interno se encarga
# de la coherencia, pero igual es buena idea copiar el dict a un dict local
# antes de ordenarlo (sorted() puede romperse si el dict cambia mientras itera).
