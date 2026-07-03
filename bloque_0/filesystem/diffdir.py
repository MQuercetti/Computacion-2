#!/usr/bin/env python3

import argparse
import hashlib
from pathlib import Path


def collect_entries(root, recursive):
    entries = {}
    if recursive:
        iterator = root.rglob("*")
    else:
        iterator = root.iterdir()
    for path in iterator:
        rel = path.relative_to(root)
        entries[str(rel)] = path
    return entries


def file_hash(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metadata_signature(path):
    stat_info = path.stat()
    return stat_info.st_size, int(stat_info.st_mtime)


def main():
    parser = argparse.ArgumentParser(description="Comparador de directorios")
    parser.add_argument("left")
    parser.add_argument("right")
    parser.add_argument("--recursive", action="store_true", help="Incluye subdirectorios")
    parser.add_argument("--checksum", action="store_true", help="Compara contenido con hash")
    args = parser.parse_args()

    left = Path(args.left)
    right = Path(args.right)

    print(f"Comparando {left} con {right}...\n")

    left_entries = collect_entries(left, args.recursive)
    right_entries = collect_entries(right, args.recursive)

    only_left = sorted(set(left_entries) - set(right_entries))
    only_right = sorted(set(right_entries) - set(left_entries))
    common = sorted(set(left_entries) & set(right_entries))

    print(f"Solo en {left}:")
    for name in only_left:
        suffix = "/" if left_entries[name].is_dir() else ""
        print(f"  {name}{suffix}")

    print(f"\nSolo en {right}:")
    for name in only_right:
        suffix = "/" if right_entries[name].is_dir() else ""
        print(f"  {name}{suffix}")

    modified_size = []
    modified_date = []
    identical = 0

    for name in common:
        left_path = left_entries[name]
        right_path = right_entries[name]
        if left_path.is_dir() and right_path.is_dir():
            identical += 1
            continue
        if left_path.is_file() and right_path.is_file():
            if args.checksum:
                if file_hash(left_path) == file_hash(right_path):
                    identical += 1
                else:
                    modified_size.append(name)
                continue
            left_size, left_mtime = metadata_signature(left_path)
            right_size, right_mtime = metadata_signature(right_path)
            if left_size != right_size:
                modified_size.append(f"{name} ({left_size} -> {right_size} bytes)")
            elif left_mtime != right_mtime:
                modified_date.append(name)
            else:
                identical += 1
        else:
            modified_size.append(name)

    print("\nModificados (tamaño diferente):")
    if modified_size:
        for item in modified_size:
            print(f"  {item}")
    else:
        print("  Ninguno")

    print("\nModificados (fecha diferente):")
    if modified_date:
        for item in modified_date:
            print(f"  {item}")
    else:
        print("  Ninguno")

    print(f"\nIdénticos: {identical} archivos")


if __name__ == "__main__":
    main()