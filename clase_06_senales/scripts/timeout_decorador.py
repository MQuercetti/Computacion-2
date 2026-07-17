#!/usr/bin/env python3
"""
timeout_decorador.py - Ejercicio 4.1 de Señales.

Decorador que agrega un timeout a una función usando SIGALRM.
Si la función tarda más que el timeout, lanza Timeout.
"""
import signal


class Timeout(Exception):
    """Excepción que se lanza cuando se agota el timeout."""
    pass


def _timeout_handler(sig, frame):
    raise Timeout("Operación excedió el tiempo límite")


def con_timeout(segundos):
    """Decorador que aplica un timeout a una función."""
    def decorador(func):
        def wrapper(*args, **kwargs):
            old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(segundos)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        return wrapper
    return decorador


@con_timeout(3)
def operacion_lenta():
    import time
    print("Iniciando operación lenta...", flush=True)
    time.sleep(5)
    return "Completado"


@con_timeout(3)
def operacion_rapida():
    import time
    print("Iniciando operación rápida...", flush=True)
    time.sleep(1)
    return "Completado"


def main():
    print("=== Operación rápida ===")
    try:
        resultado = operacion_rapida()
        print(f"Resultado: {resultado}")
    except Timeout as e:
        print(f"Timeout: {e}")

    print("\n=== Operación lenta ===")
    try:
        resultado = operacion_lenta()
        print(f"Resultado: {resultado}")
    except Timeout as e:
        print(f"Timeout: {e}")


if __name__ == "__main__":
    main()
