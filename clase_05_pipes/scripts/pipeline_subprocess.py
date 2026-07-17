#!/usr/bin/env python3
"""
pipeline_subprocess.py - Ejercicio 6.2 de Pipes.

Equivalente a `echo $texto | grep error | wc -l` pero usando
subprocess.Popen en Python.

Prerequisito: solo Linux/macOS (depende de grep/wc).
"""
import subprocess


def main():
    texto = """
primera linea
segunda linea con error
tercera linea
otra linea con error
ultima linea
"""

    echo = subprocess.Popen(["echo", texto], stdout=subprocess.PIPE)
    grep = subprocess.Popen(
        ["grep", "error"], stdin=echo.stdout, stdout=subprocess.PIPE
    )
    wc = subprocess.Popen(
        ["wc", "-l"], stdin=grep.stdout, stdout=subprocess.PIPE, text=True
    )

    # Importante: cerrar pipes del padre en el medio
    echo.stdout.close()
    grep.stdout.close()

    resultado, _ = wc.communicate()
    print(f"Líneas con 'error': {resultado.strip()}")


if __name__ == "__main__":
    main()
