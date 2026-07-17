"""
threads.py — analizador de la vista 4.

Por cada PID lista los TIDs en /proc/<pid>/task/ y para cada uno lee
/task/<tid>/{stat,comm}. Devuelve una lista de threads con su estado,
nombre y CPU%.
"""

import time
from .. import procfs
from ..agregador import escribir_slot


def analizar(pids, snapshot, intervalos, verbose):
    while True:
        datos = {}
        for pid in pids:
            tids = procfs.leer_tids(pid)
            if not tids and procfs.leer_status(pid) == {}:
                continue
            threads = []
            for tid in tids:
                t_stat = procfs.leer_thread_stat(pid, tid)
                comm = procfs.leer_thread_comm(pid, tid)
                if not t_stat:
                    continue
                threads.append({
                    "tid": tid,
                    "comm": comm,
                    "estado": t_stat["state"],
                    "utime": t_stat["utime"],
                    "stime": t_stat["stime"],
                    "cpu_pct": 0.0,  # TODO: calcular con delta
                })
            datos[pid] = threads

        escribir_slot(snapshot, "threads", datos)
        time.sleep(max(0.1, intervalos["threads"].value))


# TODO: igual que en resumen, calcular CPU% por thread necesita dos lecturas
# y guardar la anterior. La estructura puede ser {pid: {tid: (utime_prev, stime_prev, ts_prev)}}.
# Recordá: el TID principal de un proceso == PID (es el thread líder).
