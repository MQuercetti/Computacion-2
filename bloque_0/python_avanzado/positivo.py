"""Descriptor que valida valores no negativos."""

from __future__ import annotations


class Positivo:
    """Descriptor que acepta valores mayores o iguales a cero."""

    def __init__(self, default=None):
        self.default = default
        self.name = None
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name, self.default)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} debe ser positivo")
        setattr(instance, self.storage_name, value)


if __name__ == "__main__":
    class Cuenta:
        saldo = Positivo()
        limite = Positivo(default=0)

        def __init__(self, saldo, limite=1000):
            self.saldo = saldo
            self.limite = limite

    cuenta = Cuenta(100, 500)
    print(cuenta.saldo)
    print(cuenta.limite)
