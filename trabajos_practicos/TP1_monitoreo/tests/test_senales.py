"""Tests para src.senales (self-pipe pattern)."""

import os
import signal
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import senales  # noqa: E402


def test_crear_self_pipe_devuelve_dos_fds_distintos():
    r, w = senales.crear_self_pipe()
    try:
        assert isinstance(r, int)
        assert isinstance(w, int)
        assert r != w
    finally:
        os.close(r)
        os.close(w)


def test_leer_signal_no_bloqueante_devuelve_none_si_no_hay_nada():
    r, w = senales.crear_self_pipe()
    try:
        os.set_blocking(r, False)
        # Sin escribir nada, leer debe devolver None inmediatamente.
        assert senales.leer_signal_no_bloqueante(r) is None
    finally:
        os.close(r)
        os.close(w)


def test_leer_signal_no_bloqueante_devuelve_byte_escrito():
    r, w = senales.crear_self_pipe()
    try:
        os.set_blocking(r, False)
        os.write(w, bytes([signal.SIGUSR1]))
        # SIGUSR1 = 10 en Linux. El byte leído debe ser exactamente ese valor.
        leido = senales.leer_signal_no_bloqueante(r)
        assert leido == signal.SIGUSR1
    finally:
        os.close(r)
        os.close(w)


def test_procesar_evento_reconoce_shutdown():
    """SIGINT y SIGTERM deben mappear a 'shutdown'."""
    assert senales.procesar_evento(signal.SIGINT, {}, {}, "/tmp/no.json", None) == "shutdown"
    assert senales.procesar_evento(signal.SIGTERM, {}, {}, "/tmp/no.json", None) == "shutdown"


def test_procesar_evento_toggle_verbose_con_sigusr2():
    """SIGUSR2 debe alternar el flag de verbose."""
    class FakeVerbose:
        def __init__(self):
            self.value = False
    v = FakeVerbose()
    senales.procesar_evento(signal.SIGUSR2, {}, {}, "/tmp/no.json", v)
    assert v.value is True
    senales.procesar_evento(signal.SIGUSR2, {}, {}, "/tmp/no.json", v)
    assert v.value is False


def test_procesar_evento_devuelve_accion_para_senales_desconocidas():
    """Si llega un signum que no manejamos, devolvemos un string, no explotar."""
    resultado = senales.procesar_evento(99, {}, {}, "/tmp/no.json", None)
    assert "desconocida" in resultado or "99" in resultado
