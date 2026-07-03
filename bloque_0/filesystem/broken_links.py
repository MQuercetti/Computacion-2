#!/usr/bin/env python3

import argparse
import os
from pathlib import Path


def find_broken_links(root):
    broken = []
    for current_root, dirs, files in os.walk(root):
        current = Path(current_root)
        for name in list(dirs) + files:
            candidate = current / name
            if candidate.is_symlink() and not candidate.exists():
                broken.append(candidate)
    return broken


def main():
    parser = argparse.ArgumentParser(description="Detector de enlaces simbólicos rotos")
    parser.add_argument("directory", help="Directorio a buscar")
    parser.add_argument("--delete", action="store_true", help="Ofrece borrar cada enlace roto")
    parser.add_argument("--quiet", action="store_true", help="Muestra solo el conteo")
    args = parser.parse_args()

    root = Path(args.directory)
    if not root.exists() or not root.is_dir():
        print(f"Error: no se puede acceder a '{root}'")
        raise SystemExit(1)

    broken = find_broken_links(root)

    if args.quiet:
        print(len(broken))
        return

    print(f"Buscando enlaces simbólicos rotos en {root}...\n")
    if not broken:
        print("No se encontraron enlaces rotos")
        print("\nTotal: 0 enlaces rotos")
        return

    print("Enlaces rotos encontrados:")
    for link in broken:
        target = os.readlink(link)
        print(f"  {link} -> {target} (no existe)")
        if args.delete:
            answer = input(f"¿Borrar {link}? [s/N] ").strip().lower()
            if answer in {"s", "si", "y", "yes"}:
                try:
                    link.unlink()
                    print("  Eliminado")
                except OSError as error:
                    print(f"  Error: {error}")

    print(f"\nTotal: {len(broken)} enlaces rotos")


if __name__ == "__main__":
    main()