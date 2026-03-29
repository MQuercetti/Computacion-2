import argparse
import sys
from pathlib import Path


def normalizar_extension(extension):
    if extension is None:
        return None
    if extension.startswith("."):
        return extension
    return f".{extension}"


def main():
    parser = argparse.ArgumentParser(description="Version simplificada de ls")
    parser.add_argument(
        "directorio",
        nargs="?",
        default=".",
        help="Directorio a listar (por defecto: actual)",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Incluye archivos ocultos",
    )
    parser.add_argument(
        "--extension",
        help="Filtra por extension (ej: py o .py)",
    )

    args = parser.parse_args()
    ruta = Path(args.directorio)
    extension = normalizar_extension(args.extension)

    if not ruta.exists() or not ruta.is_dir():
        print(f"Error: No se puede acceder a '{ruta}'")
        sys.exit(1)

    try:
        elementos = sorted(ruta.iterdir(), key=lambda item: item.name.lower())
    except OSError:
        print(f"Error: No se puede acceder a '{ruta}'")
        sys.exit(1)

    for elemento in elementos:
        nombre = elemento.name

        if not args.all and nombre.startswith("."):
            continue

        if extension is not None and elemento.suffix != extension:
            continue

        if elemento.is_dir():
            print(f"{nombre}/")
        else:
            print(nombre)


if __name__ == "__main__":
    main()
