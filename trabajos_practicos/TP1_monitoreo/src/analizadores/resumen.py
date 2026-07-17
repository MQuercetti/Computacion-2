"""
resumen.py — analizador de la vista 1.

Lee por cada PID: /proc/<pid>/{stat,status,cmdline} y arma un dict con:
    pid, ppid, usuario, estado, comando, threads, cpu_pct

Por ahora el stub devuelve los campos básicos y deja CPU% en 0.0.
"""

import time
from .. import procfs
from ..agregador import escribir_slot


def analizar(pids, snapshot, intervalos, verbose):
    """Loop del analizador de resumen.

    Duerme según el intervalo del slot 'resumen' y reescribe el slot completo.
    """
    # El PID del propio monitor también entra en /proc — lo registramos pero
    # el display lo filtra si quiere.
    while True:
        datos = {}
        for pid in pids:
            stat = procfs.leer_stat(pid)
            status = procfs.leer_status(pid)
            cmdline = procfs.leer_cmdline(pid)

            if not stat:
                continue  # proceso desapareció entre la lista y acá

            datos[pid] = {
                "pid": stat["pid"],
                "ppid": stat["ppid"],
                "estado": stat["state"],
                "comm": stat["comm"],
                "comando": cmdline[:120],
                "threads": int(status.get("Threads", 0)) or 0,
                "uid": status.get("Uid", "?").split()[0],
                "utime": stat["utime"],
                "stime": stat["stime"],
                "cpu_pct": 0.0,  # TODO: calcular con delta de jiffies
            }

        escribir_slot(snapshot, "resumen", datos)

        # Dormimos respetando el intervalo ajustable por el display.
        tiempo = max(0.1, intervalos["resumen"].value)
        time.sleep(tiempo)


# TODO: para calcular CPU% necesitás DOS lecturas separadas en el tiempo.
# Sugerencia: mantener un dict {pid: (utime_anterior, stime_anterior, ts_anterior)}
# entre iteraciones de este loop. Calcular (delta_jiffies) / (delta_segundos * n_cpus) * 100.
#
# n_cpus sale de os.cpu_count() o de leer /proc/cpuinfo.
# El primer sample siempre da 0.0 (no hay delta) — eso es esperado y NO es un bug.
