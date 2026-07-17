"""
scheduling.py — analizador de la vista 6.

Lee de /proc/<pid>/stat los campos:
    18 → priority
    19 → nice
    40 → rt_priority
    41 → policy (0=OTHER, 1=FIFO, 2=RR, 3=BATCH, 4=IDLE, 5=DEADLINE)
y de /proc/<pid>/status:
    Cpus_allowed_list (afinidad de CPU)
    voluntary_ctxt_switches
    nonvoluntary_ctxt_switches
y campos 6,7 de stat → SID y PGID.
"""

import time
from .. import procfs
from ..agregador import escribir_slot


POLICIES = {
    0: "OTHER (SCHED_NORMAL)",
    1: "FIFO (RT)",
    2: "RR (RT round-robin)",
    3: "BATCH",
    4: "IDLE",
    5: "DEADLINE",
    6: "DEADLINE",
}


def analizar(pids, snapshot, intervalos, verbose):
    while True:
        datos = {}
        for pid in pids:
            stat = procfs.leer_stat(pid)
            status = procfs.leer_status(pid)
            if not stat:
                continue

            datos[pid] = {
                "priority": stat.get("priority", 0),
                "nice": stat.get("nice", 0),
                "rt_priority": stat.get("rt_priority", 0),
                "policy_code": stat.get("policy", 0),
                "policy_nombre": POLICIES.get(stat.get("policy", 0), "?"),
                "cpus_allowed": status.get("Cpus_allowed_list", "?"),
                "voluntary_ctxt": _parse_int(status.get("voluntary_ctxt_switches", "0")),
                "nonvoluntary_ctxt": _parse_int(status.get("nonvoluntary_ctxt_switches", "0")),
                "sid": stat.get("session", 0),
                "pgid": stat.get("pgrp", 0),
            }

        escribir_slot(snapshot, "scheduling", datos)
        time.sleep(max(0.1, intervalos["scheduling"].value))


def _parse_int(texto):
    try:
        return int(texto)
    except ValueError:
        return 0


# TODO: la consigna te puede preguntar "¿Qué es un context switch involuntario
# y por qué los procesos CPU-bound tienen muchos?". La respuesta está en
# voluntary vs nonvoluntary: involuntario = el kernel le sacó la CPU porque
# se le acabó su time slice; voluntario = el proceso solito soltó la CPU
# (por ejemplo, esperando I/O). Un proceso que está 100% en CPU sin hacer
# I/O genera muchos involuntarios.
#
# Mostralo en la vista con una columnita: "v_ctx / nv_ctx".
