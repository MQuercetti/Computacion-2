"""Decorador que valida tipos a partir de anotaciones."""

from __future__ import annotations

import inspect
import types
from functools import wraps
from typing import Any, Union, get_args, get_origin, get_type_hints


def _type_name(annotation) -> str:
    if annotation is Any:
        return "Any"
    if hasattr(annotation, "__name__"):
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def _matches_type(value, annotation) -> bool:
    if annotation is Any or annotation is inspect._empty:
        return True

    origin = get_origin(annotation)
    if origin in (Union, types.UnionType):
        return any(_matches_type(value, option) for option in get_args(annotation))

    if origin is list:
        return isinstance(value, list)
    if origin is tuple:
        return isinstance(value, tuple)
    if origin is dict:
        return isinstance(value, dict)
    if origin is set:
        return isinstance(value, set)

    if annotation is type(None):
        return value is None

    try:
        return isinstance(value, annotation)
    except TypeError:
        return True


def validate_types(funcion):
    """Valida argumentos y retorno según las anotaciones de `funcion`."""
    signature = inspect.signature(funcion)
    hints = get_type_hints(funcion)

    @wraps(funcion)
    def wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            annotation = hints.get(name, signature.parameters[name].annotation)
            if not _matches_type(value, annotation):
                expected = _type_name(annotation)
                received = type(value).__name__
                raise TypeError(f"'{name}' debe ser {expected}, recibido {received}")

        resultado = funcion(*args, **kwargs)

        return_annotation = hints.get("return", signature.return_annotation)
        if return_annotation is not inspect._empty and not _matches_type(resultado, return_annotation):
            expected = _type_name(return_annotation)
            received = type(resultado).__name__
            raise TypeError(f"retorno debe ser {expected}, recibido {received}")

        return resultado

    return wrapper


if __name__ == "__main__":
    @validate_types
    def sumar(a: int, b: int) -> int:
        return a + b

    print(sumar(1, 2))
