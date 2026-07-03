"""Timer como context manager de clase y con @contextmanager."""

from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter


class Timer:
    """Mide el tiempo de ejecución de un bloque with."""

    def __init__(self, nombre: str | None = None):
        self.nombre = nombre
        self._start = None
        self._end = None

    @property
    def elapsed(self) -> float:
        """Devuelve el tiempo transcurrido hasta ahora."""
        if self._start is None:
            return 0.0
        end = self._end if self._end is not None else perf_counter()
        return end - self._start

    def __enter__(self):
        self._start = perf_counter()
        self._end = None
        return self

    def __exit__(self, exc_type, exc, tb):
        self._end = perf_counter()
        if self.nombre:
            print(f"[Timer] {self.nombre}: {self.elapsed:.3f}s")
        return False


class _TimerState:
    """Estado compartido para la versión con @contextmanager."""

    def __init__(self, nombre: str | None = None):
        self.nombre = nombre
        self._start = None
        self._end = None

    @property
    def elapsed(self) -> float:
        if self._start is None:
            return 0.0
        end = self._end if self._end is not None else perf_counter()
        return end - self._start


@contextmanager
def timer(nombre: str | None = None):
    """Versión con @contextmanager del timer."""
    state = _TimerState(nombre)
    state._start = perf_counter()
    try:
        yield state
    finally:
        state._end = perf_counter()
        if nombre:
            print(f"[Timer] {nombre}: {state.elapsed:.3f}s")


if __name__ == "__main__":
    with Timer("Demo clase"):
        sum(range(100000))

    with timer() as t:
        sum(range(100000))
        print(f"Tiempo parcial: {t.elapsed:.3f}s")
