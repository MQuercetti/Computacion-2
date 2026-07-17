"""
agregador.py — funciones helper para escribir el slot de cada analizador
en el snapshot global de forma "atómica" desde el punto de vista lógico.

La "atomicidad" acá es lógica, no de CPU: el Manager.dict de multiprocessing
ya está sincronizado por debajo, así que un dict[clave] = valor es atómico.

El "lock" que usamos es para coordinar cosas más grandes: por ejemplo, que
el analizador de "resumen" no esté reescribiendo mientra el display lo está
leyendo para mostrar CPU%. Para el dict de shared, la sincronización interna
del Manager alcanza.

El Lock de multiprocessing es para los Value compartidos (los intervalos
ajustables con + / -): si dos hilos o procesos los modifican a la vez, el
double-write puede corromper el double.
"""

import time
from multiprocessing import Lock, Manager


# Claves del snapshot: una por analizador.
SLOTS = ("resumen", "memoria", "fds", "threads", "senales",
         "scheduling", "sistema")


def crear_snapshot():
    """Crea el Manager y el dict compartido que todos los procesos van a leer/escribir.

    Devuelve (manager, snapshot). El manager hay que mantenerlo vivo en el
    proceso padre (main.py) — si se pierde, los hijos empiezan a fallar.
    """
    mgr = Manager()
    snap = mgr.dict()
    # Inicializar cada slot con un dict vacío + timestamp 0.
    for slot in SLOTS:
        snap[slot] = {"ts": 0, "datos": {}}
    return mgr, snap


def escribir_slot(snapshot, slot, datos):
    """Sobrescribe el slot completo con un nuevo dict de datos.

    Patrón "snapshot completo": el analizador arma un dict nuevo y lo escribe
    de una. Es más simple que actualizar campo a campo y no pierde的性能
    frente a escrituras incrementales.
    """
    if slot not in SLOTS:
        raise ValueError(f"Slot desconocido: {slot}")
    snapshot[slot] = {"ts": time.time(), "datos": datos}


def leer_slot(snapshot, slot):
    """Devuelve (timestamp, datos) o (0, {}) si el slot está vacío."""
    contenido = snapshot.get(slot, {})
    return contenido.get("ts", 0), contenido.get("datos", {})


def crear_intervalos(valores_iniciales):
    """Crea un Manager + dict de Value('d') para los intervalos de cada vista.

    Devuelve (manager, dict_de_values). El dict_de_values tiene una entrada
    por slot; cada valor es un multiprocessing.Value('d', intervalo_segundos).
    El display puede modificarlo con `intervalos['resumen'].value = 0.5` y
    el analizador correspondiente lo lee en cada ciclo.
    """
    mgr = Manager()
    intervalos = mgr.dict()
    for slot, valor in valores_iniciales.items():
        intervalos[slot] = mgr.Value("d", float(valor))
    return mgr, intervalos


def crear_lock_global():
    """Lock compartido para coordinar secciones críticas que cruzan slots."""
    return Lock()
