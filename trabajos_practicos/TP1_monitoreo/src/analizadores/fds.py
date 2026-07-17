"""
fds.py — analizador de la vista 3.

Lee /proc/<pid>/fd/ y devuelve una lista de (n, destino) por cada PID.
El stub devuelve la lista cruda; el tipado (tty/socket/pipe/file) se hace
en la vista.
"""

import time
from .. import procfs
from ..agregador import escribir_slot


def analizar(pids, snapshot, intervalos, verbose):
    while True:
        datos = {}
        for pid in pids:
            fds = procfs.leer_fds(pid)
            if not fds and procfs.leer_status(pid) == {}:
                continue
            datos[pid] = [
                {"n": n, "destino": destino, "tipo": _tipo_basico(destino)}
                for n, destino in fds
            ]

        escribir_slot(snapshot, "fds", datos)
        time.sleep(max(0.1, intervalos["fds"].value))


def _tipo_basico(destino):
    """Heurística MUY básica para tipar el FD según el destino del symlink."""
    if destino.startswith("socket:"):
        return "socket"
    if destino.startswith("pipe:"):
        return "pipe"
    if destino.startswith("/dev/tty") or destino.startswith("/dev/pts"):
        return "tty"
    if destino.startswith("/"):
        return "file"
    if destino.startswith("anon_inode:"):
        return "anon_inode"
    return "?"


# TODO: mejorar el tipado. Por ejemplo:
#   - FDs 0, 1, 2 usualmente son tty/pipe.
#   - "socket:[12345]" — el 12345 es el inode; podrías mapearlo a un proceso
#     buscando en /proc/*/fd/* otro symlink con el mismo "[12345]".
#   - En modo verbose (toggle con SIGUSR2) mostrar TODOS los FDs; en modo
#     normal mostrar solo los primeros 10 o 20.
