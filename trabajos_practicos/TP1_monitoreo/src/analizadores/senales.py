"""
senales.py — analizador de la vista 5.

Lee de /proc/<pid>/status las líneas:
    SigBlk   (señales bloqueadas por el proceso)
    SigIgn   (ignoradas)
    SigCgt   (con handler propio)
    SigPnd   (pendientes en el proceso)
    ShdPnd   (pendientes en el grupo)

Son máscaras hex de 64 bits. La consigna pide que las decodifiquemos a
nombres legibles (SIGTERM, SIGINT, etc.).
"""

import time
from .. import procfs
from ..agregador import escribir_slot


def analizar(pids, snapshot, intervalos, verbose):
    while True:
        datos = {}
        for pid in pids:
            status = procfs.leer_status(pid)
            if not status:
                continue
            datos[pid] = {
                "SigBlk": status.get("SigBlk", "0"),
                "SigIgn": status.get("SigIgn", "0"),
                "SigCgt": status.get("SigCgt", "0"),
                "SigPnd": status.get("SigPnd", "0"),
                "ShdPnd": status.get("ShdPnd", "0"),
                "SigBlk_nombres": procfs.decodificar_mascara_senales(status.get("SigBlk", "0")),
                "SigIgn_nombres": procfs.decodificar_mascara_senales(status.get("SigIgn", "0")),
                "SigCgt_nombres": procfs.decodificar_mascara_senales(status.get("SigCgt", "0")),
            }

        escribir_slot(snapshot, "senales", datos)
        time.sleep(max(0.1, intervalos["senales"].value))
