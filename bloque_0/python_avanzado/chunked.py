"""Generador lazy que divide cualquier iterable en chunks de tamaño fijo."""

from __future__ import annotations

from typing import Iterable, Iterator, List, TypeVar


T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """Yield de listas con hasta `size` elementos desde cualquier iterable."""
    if size <= 0:
        raise ValueError("size debe ser mayor que 0")

    iterator = iter(iterable)
    while True:
        chunk: List[T] = []
        try:
            for _ in range(size):
                chunk.append(next(iterator))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk


if __name__ == "__main__":
    print(list(chunked(range(10), 3)))
    print(list(chunked("abcdefgh", 3)))
