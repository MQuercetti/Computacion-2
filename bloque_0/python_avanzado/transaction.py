"""Context manager que revierte cambios si ocurre una excepción."""

from __future__ import annotations

from copy import deepcopy


class Transaction:
    """Guarda el estado de un objeto y lo restaura si falla el bloque."""

    def __init__(self, objeto):
        self.objeto = objeto
        self._snapshot = None

    def __enter__(self):
        self._snapshot = deepcopy(vars(self.objeto))
        return self.objeto

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            estado = vars(self.objeto)
            estado.clear()
            estado.update(deepcopy(self._snapshot))
        return False


if __name__ == "__main__":
    class Cuenta:
        def __init__(self, saldo):
            self.saldo = saldo
            self.nombre = "Sin nombre"

    cuenta = Cuenta(1000)
    try:
        with Transaction(cuenta):
            cuenta.saldo -= 100
            cuenta.nombre = "Test"
            raise ValueError("Error simulado")
    except ValueError:
        pass
    print(cuenta.saldo, cuenta.nombre)
