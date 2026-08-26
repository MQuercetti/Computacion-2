"""
threads.py — analizador de la vista 4.

Por cada PID lista los TIDs en /proc/<pid>/task/ y para cada uno lee
/task/<tid>/{stat,comm}. Devuelve una lista de threads con su estado,
nombre y CPU%.
"""

import os
import time
from .. import procfs
from ..agregador import escribir_slot


def analizar(pids, snapshot, intervalos, verbose):
    """Loop del analizador de threads.

    CPU% por thread usa la misma fórmula que resumen (delta_jiffies /
    delta_segundos * n_cpus * 100). El estado `prev` es local al proceso
    y guarda (utime, stime, ts) por (pid, tid). El TID principal de un
    proceso == PID (thread líder).
    """
    n_cpus = os.cpu_count() or 1
    # utime/stime de /proc/<pid>/task/<tid>/stat vienen en jiffies; los pasamos
    # a segundos dividiendo por hz (SC_CLK_TCK) antes de calcular el %.
    hz = os.sysconf("SC_CLK_TCK")
    prev = {}  # {pid: {tid: (utime_prev, stime_prev, ts_prev)}}

    while True:
        datos = {}
        ahora = time.time()
        pids_vistos = set(pids)  # snapshot actual: claves que deben quedar en prev
        for pid in pids:
            tids = procfs.leer_tids(pid)
            if not tids and procfs.leer_status(pid) == {}:
                continue
            threads = []
            tids_vistos = set(tids)  # snapshot de tids: claves que deben quedar en prev[pid]
            if pid not in prev:
                prev[pid] = {}
            for tid in tids:
                t_stat = procfs.leer_thread_stat(pid, tid)
                comm = procfs.leer_thread_comm(pid, tid)
                if not t_stat:
                    continue
                utime = t_stat["utime"]
                stime = t_stat["stime"]
                cpu_pct = 0.0
                if tid in prev[pid]:
                    utime_p, stime_p, ts_p = prev[pid][tid]
                    dt = ahora - ts_p
                    if dt > 0:
                        dj = (utime + stime) - (utime_p + stime_p)
                        # dj está en jiffies → dividir por hz para tener segundos.
                        cpu_pct = round(100.0 * (dj / hz) / (dt * n_cpus), 2)
                prev[pid][tid] = (utime, stime, ahora)
                threads.append({
                    "tid": tid,
                    "comm": comm,
                    "estado": t_stat["state"],
                    "utime": utime,
                    "stime": stime,
                    "cpu_pct": cpu_pct,
                })
            # Limpiar tids muertos dentro de este pid.
            for tid in list(prev[pid].keys()):
                if tid not in tids_vistos:
                    del prev[pid][tid]
            datos[pid] = threads

        # Limpiar pids muertos del nivel superior de prev.
        for pid in list(prev.keys()):
            if pid not in pids_vistos:
                del prev[pid]

        escribir_slot(snapshot, "threads", datos)
        time.sleep(max(0.1, intervalos["threads"].value))
