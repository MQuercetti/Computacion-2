"""Context manager para crear y limpiar archivos temporales nombrados."""

from contextlib import contextmanager
from pathlib import Path


@contextmanager
def archivo_temporal(nombre: str):
    """Crea un archivo temporal con el nombre indicado y lo borra al salir.

    El archivo se abre en modo lectura/escritura para que pueda escribirse y
    leerse dentro del bloque `with`.
    """
    path = Path(nombre)
    handle = path.open("w+", encoding="utf-8")
    try:
        yield handle
    finally:
        handle.close()
        try:
            path.unlink()
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    with archivo_temporal("demo_temporal.txt") as archivo:
        archivo.write("Datos de prueba\n")
        archivo.seek(0)
        print(archivo.read())
    print("Archivo borrado:", not Path("demo_temporal.txt").exists())
