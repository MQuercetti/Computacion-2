"""
resumen.py — analizador de la vista 1.

Lee por cada PID: /proc/<pid>/{stat,status,cmdline} y arma un dict con:
    pid, ppid, usuario, estado, comando, threads, cpu_pct

Por ahora el stub devuelve los campos básicos y deja CPU% en 0.0.
"""

import os
import time
from .. import procfs
from ..agregador import escribir_slot


def analizar(pids, snapshot, intervalos, verbose):
    """Loop del analizador de resumen.

    Duerme según el intervalo del slot 'resumen' y reescribe el slot completo.

    Calcula CPU% por proceso con la fórmula estándar:
        (delta_jiffies / (delta_segundos * n_cpus)) * 100

    `prev` guarda la lectura anterior en este mismo proceso (no se comparte),
    así que no necesita lock. El primer sample siempre da 0.0 — eso es
    esperado porque no hay delta.
    """
    n_cpus = os.cpu_count() or 1
    # utime/stime de /proc/<pid>/stat vienen en jiffies; los pasamos a
    # segundos dividiendo por hz (SC_CLK_TCK) antes de calcular el %.
    hz = os.sysconf("SC_CLK_TCK")
    prev = {}  # {pid: (utime_prev, stime_prev, ts_prev)}

    while True:
        datos = {}
        ahora = time.time()
        pids_vistos = set(pids)  # snapshot actual: claves que deben quedar en prev
        for pid in pids:
            stat = procfs.leer_stat(pid)
            status = procfs.leer_status(pid)
            cmdline = procfs.leer_cmdline(pid)

            if not stat:
                continue  # proceso desapareció entre la lista y acá

            utime = stat["utime"]
            stime = stat["stime"]
            cpu_pct = 0.0
            if pid in prev:
                utime_p, stime_p, ts_p = prev[pid]
                dt = ahora - ts_p
                if dt > 0:
                    dj = (utime + stime) - (utime_p + stime_p)
                    # dj está en jiffies → dividir por hz para tener segundos.
                    cpu_pct = round(100.0 * (dj / hz) / (dt * n_cpus), 2)
            prev[pid] = (utime, stime, ahora)

            datos[pid] = {
                "pid": stat["pid"],
                "ppid": stat["ppid"],
                "estado": stat["state"],
                "comm": stat["comm"],
                "comando": cmdline[:120],
                "threads": int(status.get("Threads", 0)) or 0,
                "uid": status.get("Uid", "?").split()[0],
                "utime": utime,
                "stime": stime,
                "cpu_pct": cpu_pct,
            }

        # Limpiar prev: dejar solo pids que siguen en el snapshot actual.
        for pid in list(prev.keys()):
            if pid not in pids_vistos:
                del prev[pid]

        escribir_slot(snapshot, "resumen", datos)

        # Dormimos respetando el intervalo ajustable por el display.
        tiempo = max(0.1, intervalos["resumen"].value)
        time.sleep(tiempo)
