"""Lector lazy de archivos que entrega líneas completas desde chunks."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator


class BufferedReader:
    """Lee un archivo por bloques pero itera línea por línea."""

    def __init__(self, path: str, buffer_size: int = 8192):
        if buffer_size <= 0:
            raise ValueError("buffer_size debe ser mayor que 0")
        self.path = Path(path)
        self.buffer_size = buffer_size
        self._handle = None

    def __enter__(self):
        self._handle = self.path.open("r", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._handle is not None:
            self._handle.close()
            self._handle = None
        return False

    def _iter_from_handle(self, handle) -> Iterator[str]:
        buffer = ""
        while True:
            chunk = handle.read(self.buffer_size)
            if not chunk:
                break
            buffer += chunk
            parts = buffer.splitlines(keepends=True)
            if parts and not parts[-1].endswith(("\n", "\r")):
                buffer = parts.pop()
            else:
                buffer = ""
            for line in parts:
                yield line
        if buffer:
            yield buffer

    def __iter__(self) -> Iterator[str]:
        if self._handle is not None:
            yield from self._iter_from_handle(self._handle)
            return
        with self.path.open("r", encoding="utf-8") as handle:
            yield from self._iter_from_handle(handle)


if __name__ == "__main__":
    for line in BufferedReader(__file__, buffer_size=64):
        print(line, end="")
        break
