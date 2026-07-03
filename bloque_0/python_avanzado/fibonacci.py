"""Generador de Fibonacci infinito y con límite opcional."""

from __future__ import annotations

from typing import Iterator


def fibonacci(limite: int | None = None) -> Iterator[int]:
    """Genera la secuencia de Fibonacci.

    Si `limite` es None, produce la secuencia infinita.
    Si `limite` tiene un valor numérico, genera todos los valores <= límite.
    """
    actual, siguiente = 0, 1
    while limite is None or actual <= limite:
        yield actual
        actual, siguiente = siguiente, actual + siguiente


if __name__ == "__main__":
    fib = fibonacci()
    for _ in range(10):
        print(next(fib), end=" ")
    print()
    print(list(fibonacci(limite=100)))
