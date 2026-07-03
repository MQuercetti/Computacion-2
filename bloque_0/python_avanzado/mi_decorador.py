"""Decorador flexible que funciona con y sin paréntesis."""

from __future__ import annotations

from functools import wraps


def mi_decorador(func=None, *, verbose: bool = False):
    """Envuelve una función y opcionalmente muestra mensajes."""

    def decorator(real_func):
        @wraps(real_func)
        def wrapper(*args, **kwargs):
            if verbose:
                print(f"Ejecutando {real_func.__name__}")
            return real_func(*args, **kwargs)

        return wrapper

    if func is not None and callable(func):
        return decorator(func)
    return decorator


if __name__ == "__main__":
    @mi_decorador
    def funcion1():
        return "sin paréntesis"

    @mi_decorador()
    def funcion2():
        return "con paréntesis"

    @mi_decorador(verbose=True)
    def funcion3():
        return "verbose"

    print(funcion1())
    print(funcion2())
    print(funcion3())
