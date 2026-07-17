"""
procfs.py — helpers para leer /proc directamente.

Toda la magia del monitor pasa por acá. NO usar psutil, NI subprocess a ps/top.
Cada función devuelve estructuras simples (dict / list / str) que los analizadores
pueden procesar.

Convención:
    - Si un proceso desaparece entre listar_pids() y leer_xxx(pid), devolvemos {} o [].
      Esto es normal y NO es un error: los procesos son transitorios.
    - Si un archivo no se puede leer (permisos, formato inesperado), devolvemos {} o ''.
      Los analizadores loguean y siguen.
"""

import os
import re
import time


# Nombre de las señales (1..64) para decodificar máscaras como SigBlk.
# Orden: índice 0 es señal 1 (SIGHUP), índice 63 es señal 64.
SIGNAMES = [
    # 1..31 — señales estándar POSIX/Linux
    "SIGHUP", "SIGINT", "SIGQUIT", "SIGILL", "SIGTRAP", "SIGABRT", "SIGBUS",
    "SIGFPE", "SIGKILL", "SIGUSR1", "SIGSEGV", "SIGPIPE", "SIGALRM", "SIGTERM",
    "SIGSTKFLT", "SIGCHLD", "SIGCONT", "SIGSTOP", "SIGTSTP", "SIGTTIN", "SIGTTOU",
    "SIGURG", "SIGXCPU", "SIGXFSZ", "SIGVTALRM", "SIGPROF", "SIGWINCH", "SIGIO",
    "SIGPWR", "SIGSYS",
    # 32..34 — huecos del sistema (en Linux x86 son 32, 33, 34 los huecos)
    "SIGRTMIN+0", "SIGRTMIN+1", "SIGRTMIN+2",
    # 35..50 — SIGRTMIN+3 a SIGRTMIN+15 (señales realtime, 13 señales)
    "SIGRTMIN+3", "SIGRTMIN+4", "SIGRTMIN+5", "SIGRTMIN+6", "SIGRTMIN+7",
    "SIGRTMIN+8", "SIGRTMIN+9", "SIGRTMIN+10", "SIGRTMIN+11", "SIGRTMIN+12",
    "SIGRTMIN+13", "SIGRTMIN+14",
    # El hueco de señal 47 depende de la arquitectura, en x86_64 no se usa.
    "SIGRTMAX-15",
    # 49..64 — 16 señales SIGRTMAX-n (de -14 a -1) y SIGRTMAX
    "SIGRTMAX-14", "SIGRTMAX-13", "SIGRTMAX-12", "SIGRTMAX-11", "SIGRTMAX-10",
    "SIGRTMAX-9", "SIGRTMAX-8", "SIGRTMAX-7", "SIGRTMAX-6", "SIGRTMAX-5",
    "SIGRTMAX-4", "SIGRTMAX-3", "SIGRTMAX-2", "SIGRTMAX-1",
    "SIGRTMAX",
]
# Rellenamos hasta 64 con nombres genéricos por si el mapping varía entre
# arquitecturas (lo que importa es el conteo: 64 bits = 64 señales).
while len(SIGNAMES) < 64:
    SIGNAMES.append(f"SIGRT({len(SIGNAMES) + 1})")
assert len(SIGNAMES) == 64


# Estados posibles del campo 3 de /proc/<pid>/stat.
ESTADOS = {
    "R": "Corriendo",
    "S": "Durmiendo",
    "D": "Disco (uninterruptible)",
    "Z": "Zombie",
    "T": "Detenido",
    "t": "Tracing stop",
    "I": "Idle (kernel >= 4.14)",
    "X": "Muerto",
    "K": "Wakekill",
    "W": "Waking",
    "P": "Parked",
}


def listar_pids():
    """Devuelve la lista de PIDs visibles en /proc como enteros.

    Filtramos lo que no es numérico por si hay carpetas especiales (e.g. 'sys').
    """
    pids = []
    try:
        for nombre in os.listdir("/proc"):
            if nombre.isdigit():
                pids.append(int(nombre))
    except FileNotFoundError:
        return []
    return pids


def leer_status(pid):
    """Lee /proc/<pid>/status y devuelve un dict clave:valor.

    Las líneas tienen formato "Clave:\tValor". Algunas (como SigBlk) traen
    máscaras hexadecimales de 64 bits — eso lo decodifica cada analizador.
    """
    ruta = f"/proc/{pid}/status"
    out = {}
    try:
        with open(ruta, "r") as f:
            for linea in f:
                if ":" not in linea:
                    continue
                clave, _, valor = linea.partition(":")
                out[clave.strip()] = valor.strip()
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        return {}
    return out


def leer_stat(pid):
    """Lee /proc/<pid>/stat y devuelve el dict con TODOS los campos parseados.

    /proc/<pid>/stat tiene un formato peculiar: el primer campo es "PID (comm) estado"
    donde (comm) puede contener ESPACIOS y paréntesis. Por eso no se puede split(' ')
    y hay que usar regex.

    Devuelve un dict con al menos: pid, comm, state, ppid, pgrp, session,
    utime, stime, nice, priority, rt_priority, policy, startcode, minflt, cminflt,
    majflt, cmajflt.
    """
    ruta = f"/proc/{pid}/stat"
    try:
        with open(ruta, "r") as f:
            linea = f.readline()
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        return {}

    # El comm está entre paréntesis, al final del primer "trozo" de la línea.
    # Capturamos: PID (comm) resto...
    m = re.match(r"^(\d+)\s+\((.*)\)\s+(.*)$", linea)
    if not m:
        return {}
    pid_leido = int(m.group(1))
    comm = m.group(2)
    resto = m.group(3).split()

    # resto[0] es el estado, y los índices siguientes (0-based dentro de resto)
    # corresponden a campos de man proc(5) numerados a partir del 3.
    # Mapeo: campo N de la consigna -> resto[N-3]
    try:
        return {
            "pid": pid_leido,
            "comm": comm,
            "state": resto[0],
            "ppid": int(resto[1]),         # campo 4
            "pgrp": int(resto[2]),         # campo 5 → PGID
            "session": int(resto[3]),      # campo 6 → SID
            # 7-9 son tty_nr, tpgid, flags
            "minflt": int(resto[7]),       # campo 10
            "cminflt": int(resto[8]),      # campo 11
            "majflt": int(resto[9]),       # campo 12
            "cmajflt": int(resto[10]),     # campo 13
            "utime": int(resto[11]),       # campo 14
            "stime": int(resto[12]),       # campo 15
            # 16-17 son cutime, cstime
            "priority": int(resto[15]),    # campo 18
            "nice": int(resto[16]),        # campo 19
            # 20-21 son num_threads, itrealvalue
            "starttime": int(resto[19]),   # campo 22
            # ...
            "rt_priority": int(resto[33]), # campo 40
            "policy": int(resto[34]),      # campo 41
        }
    except (IndexError, ValueError):
        return {}


def leer_cmdline(pid):
    """Lee /proc/<pid>/cmdline y devuelve el comando como string.

    cmdline tiene los argumentos separados por NUL ('\\0') y un NUL al final.
    """
    ruta = f"/proc/{pid}/cmdline"
    try:
        with open(ruta, "rb") as f:
            data = f.read()
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        return ""
    if not data:
        return ""
    return data.replace(b"\x00", b" ").decode("utf-8", errors="replace").strip()


def leer_fds(pid):
    """Lee /proc/<pid>/fd/ y devuelve lista de tuplas (n, destino).

    Cada FD es un symlink; os.readlink devuelve a qué apunta.
    """
    ruta = f"/proc/{pid}/fd"
    out = []
    try:
        for nombre in os.listdir(ruta):
            if not nombre.isdigit():
                continue
            try:
                destino = os.readlink(os.path.join(ruta, nombre))
            except (FileNotFoundError, ProcessLookupError, PermissionError):
                continue
            out.append((int(nombre), destino))
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        return []
    return out


def leer_tids(pid):
    """Devuelve la lista de TIDs (threads) de un proceso desde /proc/<pid>/task."""
    ruta = f"/proc/{pid}/task"
    try:
        return [int(t) for t in os.listdir(ruta) if t.isdigit()]
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        return []


def leer_thread_stat(pid, tid):
    """Lee /proc/<pid>/task/<tid>/stat. Devuelve dict con comm, state, utime, stime."""
    ruta = f"/proc/{pid}/task/{tid}/stat"
    try:
        with open(ruta, "r") as f:
            linea = f.readline()
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        return {}
    m = re.match(r"^(\d+)\s+\((.*)\)\s+(.*)$", linea)
    if not m:
        return {}
    resto = m.group(3).split()
    try:
        return {
            "tid": int(m.group(1)),
            "comm": m.group(2),
            "state": resto[0],
            "utime": int(resto[11]),
            "stime": int(resto[12]),
        }
    except (IndexError, ValueError):
        return {}


def leer_thread_comm(pid, tid):
    """Lee el nombre del thread (es lo que ve 'top -H')."""
    ruta = f"/proc/{pid}/task/{tid}/comm"
    try:
        with open(ruta, "r") as f:
            return f.readline().strip()
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        return ""


def leer_meminfo():
    """Lee /proc/meminfo y devuelve dict con MemTotal, MemFree, MemAvailable, etc.

    Los valores vienen en kB como strings tipo '16384000 kB'.
    """
    out = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for linea in f:
                if ":" not in linea:
                    continue
                clave, _, valor = linea.partition(":")
                partes = valor.strip().split()
                # partes[0] es el número, partes[1] la unidad (kB típicamente).
                try:
                    out[clave.strip()] = int(partes[0])
                except (ValueError, IndexError):
                    out[clave.strip()] = 0
    except FileNotFoundError:
        return {}
    return out


def leer_stat_global():
    """Lee la línea 'cpu' agregada de /proc/stat.

    Devuelve dict con: user, nice, system, idle, iowait, irq, softirq, steal, guest.
    Para CPU% global hay que calcular DELTA entre dos lecturas (no absolutos).
    """
    try:
        with open("/proc/stat", "r") as f:
            for linea in f:
                if linea.startswith("cpu "):
                    partes = linea.split()
                    campos = ["user", "nice", "system", "idle", "iowait",
                              "irq", "softirq", "steal", "guest", "guest_nice"]
                    valores = [int(x) for x in partes[1:11]]
                    return dict(zip(campos, valores))
    except (FileNotFoundError, ValueError):
        return {}
    return {}


def leer_loadavg():
    """Lee /proc/loadavg. Devuelve (1min, 5min, 15min, running/total, last_pid)."""
    try:
        with open("/proc/loadavg", "r") as f:
            partes = f.read().split()
        return {
            "1min": float(partes[0]),
            "5min": float(partes[1]),
            "15min": float(partes[2]),
            "running_total": partes[3],
        }
    except (FileNotFoundError, IndexError, ValueError):
        return {}


def leer_uptime():
    """Lee /proc/uptime. Devuelve (uptime_seg, idle_seg)."""
    try:
        with open("/proc/uptime", "r") as f:
            partes = f.read().split()
        return {"uptime": float(partes[0]), "idle": float(partes[1])}
    except (FileNotFoundError, IndexError, ValueError):
        return {}


def btime():
    """Lee btime de /proc/stat: segundos desde epoch del último boot."""
    try:
        with open("/proc/stat", "r") as f:
            for linea in f:
                if linea.startswith("btime "):
                    return int(linea.split()[1])
    except (FileNotFoundError, IndexError, ValueError):
        return 0
    return 0


def decodificar_mascara_senales(mascara_hex):
    """Decodifica una máscara de 64 bits (string hex) a lista de nombres de señales activas.

    Ej: "0000000000000000" → []
        "0000000000000002" → ['SIGINT']   (bit 1 = señal 2)

    Recordá: el bit 0 del entero corresponde a la señal 1 (SIGHUP).
    """
    if not mascara_hex:
        return []
    try:
        valor = int(mascara_hex, 16)
    except ValueError:
        return []
    activas = []
    for i in range(64):
        if valor & (1 << i):
            activas.append(SIGNAMES[i])
    return activas


# TODO: para que el monitor pueda calcular CPU% de un proceso a partir de
# /proc/<pid>/stat necesita DOS lecturas separadas en el tiempo (utime+stime
# son jiffies ACUMULADOS desde que arrancó el proceso). El analizador tiene que
# guardar la lectura anterior y calcular (delta_jiffies / delta_segundos) / n_cpus * 100.
#
# Pregunta para vos: ¿en qué estructura guardás la lectura anterior? ¿Y qué
# hacés cuando aparece un PID nuevo (no hay lectura previa)? Pista: el primer
# sample siempre devuelve 0% — eso es esperado.


# TODO: similar a lo anterior, para el CPU% global del sistema hay que leer
# /proc/stat dos veces y sacar delta de (user+nice+system) vs (total). Eso
# lo hace el analizador de sistema.


if __name__ == "__main__":
    # Mini-prueba: ver qué leemos de nuestro propio proceso.
    pids = listar_pids()
    print(f"PIDs visibles: {len(pids)}")
    if pids:
        pid = pids[0]
        print(f"\nMuestra con PID {pid}:")
        print(f"  status (claves): {list(leer_status(pid).keys())[:5]}...")
        print(f"  stat: {leer_stat(pid)}")
        print(f"  cmdline: {leer_cmdline(pid)[:80]}")
        print(f"  meminfo total kB: {leer_meminfo().get('MemTotal', '?')}")
        print(f"  loadavg: {leer_loadavg()}")
