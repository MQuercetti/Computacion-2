"""
memoria.py — analizador de la vista 2.

Lee por cada PID: /proc/<pid>/{status,maps} y arma un dict con:
    vm_size, vm_rss, vm_data, vm_stk, vm_exe, vm_lib, vm_hwm, vm_swap,
    minflt, majflt, segmentos (text/data/heap/stack/shared)

El stub devuelve VmRSS y VmSize; el resto se va completando.
"""

import time
from .. import procfs
from ..agregador import escribir_slot


def analizar(pids, snapshot, intervalos, verbose):
    while True:
        datos = {}
        for pid in pids:
            status = procfs.leer_status(pid)
            stat = procfs.leer_stat(pid)
            if not status:
                continue

            datos[pid] = {
                "vm_size": _parse_kb(status.get("VmSize", "0 kB")),
                "vm_rss": _parse_kb(status.get("VmRSS", "0 kB")),
                "vm_data": _parse_kb(status.get("VmData", "0 kB")),
                "vm_stk": _parse_kb(status.get("VmStk", "0 kB")),
                "vm_exe": _parse_kb(status.get("VmExe", "0 kB")),
                "vm_lib": _parse_kb(status.get("VmLib", "0 kB")),
                "vm_hwm": _parse_kb(status.get("VmHWM", "0 kB")),
                "vm_swap": _parse_kb(status.get("VmSwap", "0 kB")),
                "minflt": stat.get("minflt", 0),
                "majflt": stat.get("majflt", 0),
                "segmentos": {},  # TODO: parsear /proc/<pid>/maps
            }

        escribir_slot(snapshot, "memoria", datos)
        time.sleep(max(0.1, intervalos["memoria"].value))


def _parse_kb(texto):
    """Convierte '1234 kB' → 1234 (int). Si no se puede, devuelve 0."""
    try:
        return int(texto.split()[0])
    except (ValueError, IndexError):
        return 0


# TODO: leer /proc/<pid>/maps y agrupar por permisos y por nombre ([heap],
# [stack], [vdso], etc). Cada línea tiene formato:
#   dirección_permisos offset dev inode nombre
#   ej: 55a8b2a00000-55a8b2a21000 r--p 00000000 08:01 1234                       /usr/bin/python3
# Agrupar las que tengan el mismo path o nombre de sección y sumar tamaños.
