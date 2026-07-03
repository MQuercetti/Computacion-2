"""Scheduler round-robin simple basado en generadores."""

from __future__ import annotations

from collections import deque


class Scheduler:
    """Ejecuta generadores cooperativos un paso por vez."""

    def __init__(self):
        self._tasks = deque()

    def add(self, task):
        """Agrega un generador o iterador a la cola."""
        self._tasks.append(iter(task))

    def run(self):
        """Ejecuta todas las tareas hasta agotarlas."""
        while self._tasks:
            task = self._tasks.popleft()
            try:
                next(task)
            except StopIteration:
                continue
            self._tasks.append(task)


if __name__ == "__main__":
    def tarea_a():
        for i in range(3):
            print(f"Tarea A: paso {i}")
            yield

    def tarea_b():
        for i in range(5):
            print(f"Tarea B: paso {i}")
            yield

    scheduler = Scheduler()
    scheduler.add(tarea_a())
    scheduler.add(tarea_b())
    scheduler.run()
