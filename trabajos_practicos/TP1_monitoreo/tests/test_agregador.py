"""Tests para src.agregador (snapshot compartido e intervalos)."""

import multiprocessing as mp
import time

import pytest

from src.agregador import (
    SLOTS,
    crear_intervalos,
    crear_lock_global,
    crear_snapshot,
    escribir_slot,
    leer_slot,
)


def test_slots_contiene_las_7_vistas_obligatorias():
    """La consigna exige 7 analizadores: resumen, memoria, fds, threads, senales, scheduling, sistema."""
    assert len(SLOTS) == 7
    assert set(SLOTS) == {"resumen", "memoria", "fds", "threads", "senales", "scheduling", "sistema"}


def test_crear_snapshot_inicializa_los_7_slots_vacios():
    mgr, snap = crear_snapshot()
    try:
        assert set(snap.keys()) == set(SLOTS)
        for slot in SLOTS:
            assert snap[slot] == {"ts": 0, "datos": {}}
    finally:
        mgr.shutdown()


def test_escribir_y_leer_slot_roundtrip():
    mgr, snap = crear_snapshot()
    try:
        datos = {1: {"pid": 1, "comm": "init", "cpu_pct": 0.5}}
        escribir_slot(snap, "resumen", datos)
        ts, leido = leer_slot(snap, "resumen")
        assert ts > 0
        assert leido == datos
    finally:
        mgr.shutdown()


def test_escribir_slot_rechaza_nombre_invalido():
    mgr, snap = crear_snapshot()
    try:
        with pytest.raises(ValueError, match="Slot desconocido"):
            escribir_slot(snap, "inventado", {})
    finally:
        mgr.shutdown()


def test_leer_slot_inexistente_devuelve_vacio():
    mgr, snap = crear_snapshot()
    try:
        ts, datos = leer_slot(snap, "no_existe")
        assert ts == 0
        assert datos == {}
    finally:
        mgr.shutdown()


def test_crear_intervalos_usa_valores_iniciales():
    cfg = {"resumen": 1.5, "memoria": 2.5, "fds": 5.0}
    mgr, intervalos = crear_intervalos(cfg)
    try:
        assert intervalos["resumen"].value == 1.5
        assert intervalos["memoria"].value == 2.5
        assert intervalos["fds"].value == 5.0
    finally:
        mgr.shutdown()


def test_lock_global_se_puede_adquirir_y_liberar():
    lock = crear_lock_global()
    adquirido = lock.acquire(block=True, timeout=1)
    assert adquirido is True
    lock.release()
