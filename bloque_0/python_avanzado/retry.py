"""Decorador de reintentos para operaciones que pueden fallar."""

from __future__ import annotations

from functools import wraps
from time import sleep


def retry(max_attempts: int = 3, delay: float = 1, exceptions=(Exception,)):
    """Reintenta una función si lanza una de las excepciones configuradas."""

    def decorator(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return funcion(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt == max_attempts:
                        print(f"Intento {attempt}/{max_attempts} falló: {exc}.")
                        raise
                    print(f"Intento {attempt}/{max_attempts} falló: {exc}. Esperando {delay}s...")
                    sleep(delay)
            raise last_exception  # pragma: no cover

        return wrapper

    return decorator


if __name__ == "__main__":
    import random

    @retry(max_attempts=3, delay=0.1, exceptions=(ConnectionError,))
    def conectar_servidor():
        if random.random() < 0.7:
            raise ConnectionError("Servidor no disponible")
        return "Conectado exitosamente"

    try:
        print(conectar_servidor())
    except ConnectionError:
        print("Falló después de 3 intentos")
