"""Paquete de ejecutores de tareas."""
from .cpu_bound import compute_iterative_hash
from .io_bound import ejecutar_descargas
from .simulated import ejecutar_espera

__all__ = ["compute_iterative_hash", "ejecutar_descargas", "ejecutar_espera"]
