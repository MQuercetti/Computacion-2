"""Metaclase Singleton que garantiza una sola instancia por clase."""

from __future__ import annotations


class Singleton(type):
    """Metaclase que reutiliza la primera instancia creada."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


if __name__ == "__main__":
    class Configuracion(metaclass=Singleton):
        def __init__(self, debug=False):
            self.debug = debug

    c1 = Configuracion(debug=True)
    c2 = Configuracion(debug=False)
    print(c1 is c2)
    print(c1.debug)
