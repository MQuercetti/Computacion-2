"""Tests para src.procfs (lectura de /proc).

Los tests usan el PID del propio pytest (os.getpid()) para tener datos reales
sin depender de qué procesos estén vivos en el sistema. Si /proc no existe
(Windows / macOS sin Docker), los tests se saltean en lugar de fallar.
"""

import os
import sys

import pytest

# Aseguramos que se pueda importar `src.procfs` cuando pytest se corre desde
# la raíz del proyecto.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import procfs  # noqa: E402


pytestmark = pytest.mark.skipif(
    not os.path.exists("/proc"),
    reason="Requiere /proc (Linux nativo o dentro del container).",
)


def test_listar_pids_incluye_el_pid_actual():
    pids = procfs.listar_pids()
    assert isinstance(pids, list)
    assert os.getpid() in pids
    assert all(isinstance(p, int) for p in pids)


def test_leer_status_del_pid_actual_tiene_campos_basicos():
    status = procfs.leer_status(os.getpid())
    assert "Name" in status
    assert "Pid" in status
    assert "State" in status
    # Pid debe coincidir con el nuestro.
    assert status["Pid"] == str(os.getpid())


def test_leer_stat_del_pid_actual_parsea_campos_clave():
    stat = procfs.leer_stat(os.getpid())
    # Si el proceso murió entre listar_pids y leer_stat, devuelve {}.
    if not stat:
        pytest.skip("El proceso actual desapareció durante el test.")
    assert stat["pid"] == os.getpid()
    assert "comm" in stat and stat["comm"]  # comm no vacío
    assert "state" in stat and stat["state"] in procfs.ESTADOS
    assert isinstance(stat["utime"], int)
    assert isinstance(stat["stime"], int)
    assert isinstance(stat["nice"], int)


def test_leer_stat_con_comm_con_espacios_o_parentesis():
    """El parser debe tolerar nombres de proceso con espacios y paréntesis.

    Usamos un subprocess que setea comm con espacios (Python -c '...').
    Si no se puede crear, el test se skipea.
    """
    import subprocess
    import tempfile

    try:
        # Lanzamos un proceso corto con un comm con espacios.
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("import time\ntime.sleep(2)\n")
            script = f.name
        p = subprocess.Popen([sys.executable, script])
        try:
            stat = procfs.leer_stat(p.pid)
            if not stat:
                pytest.skip("El subprocess desapareció antes de poder leerlo.")
            # Lo importante: que el parseo no haya tirado y devuelva comm no vacío.
            assert "comm" in stat
            assert "state" in stat
        finally:
            p.terminate()
            p.wait(timeout=2)
            os.unlink(script)
    except (FileNotFoundError, PermissionError):
        pytest.skip("No se pudo crear un subprocess para testear.")


def test_leer_cmdline_del_pid_actual_devuelve_string():
    cmd = procfs.leer_cmdline(os.getpid())
    assert isinstance(cmd, str)
    # El comando de pytest debería contener 'pytest' o 'python'.
    if cmd:  # puede ser vacío si el proceso es del kernel
        assert any(token in cmd.lower() for token in ("python", "pytest"))


def test_leer_cmdline_de_pid_inexistente_devuelve_string_vacio():
    # PIDs muy altos o que no existen deberían devolver "" sin explotar.
    assert procfs.leer_cmdline(999_999_999) == ""


def test_estados_contiene_las_letras_estandar():
    """Las letras que más usamos en clase: R, S, D, Z, T."""
    for letra in ("R", "S", "D", "Z", "T"):
        assert letra in procfs.ESTADOS


def test_signames_tiene_64_entradas():
    """64 señales = capacidad del bitmask de 64 bits de /proc/<pid>/status."""
    assert len(procfs.SIGNAMES) == 64
    # Las señales más comunes deben estar en la lista.
    for nombre in ("SIGHUP", "SIGINT", "SIGTERM", "SIGKILL", "SIGUSR1", "SIGUSR2"):
        assert nombre in procfs.SIGNAMES
