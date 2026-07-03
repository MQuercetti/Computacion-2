"""Decorador que registra llamadas a funciones con timestamp."""

from __future__ import annotations

from datetime import datetime
from functools import wraps


def _formatear_llamada(nombre: str, args: tuple, kwargs: dict) -> str:
    partes = [repr(arg) for arg in args]
    partes.extend(f"{clave}={valor!r}" for clave, valor in kwargs.items())
    return f"{nombre}({', '.join(partes)})"


def log_llamada(funcion):
    """Imprime una línea antes y después de ejecutar `funcion`."""

    @wraps(funcion)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Llamando a {_formatear_llamada(funcion.__name__, args, kwargs)}")
        resultado = funcion(*args, **kwargs)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {funcion.__name__} retornó {resultado!r}")
        return resultado

    return wrapper


if __name__ == "__main__":
    @log_llamada
    def sumar(a, b):
        return a + b

    @log_llamada
    def saludar(nombre, entusiasta=False):
        sufijo = "!" if entusiasta else "."
        return f"Hola, {nombre}{sufijo}"

    sumar(3, 5)
    saludar("Ana", entusiasta=True)
