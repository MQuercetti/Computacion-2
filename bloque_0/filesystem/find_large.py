#!/usr/bin/env python3

import argparse
import fnmatch
import os
from pathlib import Path


def parse_size(text):
    multipliers = {"K": 1024, "M": 1024 ** 2, "G": 1024 ** 3}
    if not text:
        return 0
    suffix = text[-1].upper()
    if suffix in multipliers:
        return int(float(text[:-1]) * multipliers[suffix])
    return int(text)


def human_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} B"
            return f"{value:.1f} {unit}" if value < 10 else f"{value:.0f} {unit}"
        value /= 1024


def size_of_path(path, cache):
    if path in cache:
        return cache[path]
    try:
        if path.is_symlink():
            cache[path] = 0
            return 0
        if path.is_file():
            cache[path] = path.stat().st_size
            return cache[path]
        if path.is_dir():
            total = 0
            for child in path.iterdir():
                total += size_of_path(child, cache)
            cache[path] = total
            return total
    except OSError:
        return 0
    cache[path] = 0
    return 0


def matches_type(path, wanted_type):
    if wanted_type == "f":
        return path.is_file()
    if wanted_type == "d":
        return path.is_dir()
    return True


def walk(directory):
    for root, dirs, files in os.walk(directory):
        current = Path(root)
        yield current
        for name in files:
            yield current / name


def main():
    parser = argparse.ArgumentParser(description="Buscador de archivos grandes")
    parser.add_argument("directory", help="Directorio a analizar")
    parser.add_argument("--min-size", default="0", help="Tamaño mínimo (ej: 100K, 1M, 2G)")
    parser.add_argument("--type", choices=["f", "d"], help="Filtra por tipo")
    parser.add_argument("--top", type=int, help="Muestra solo los N más grandes")
    args = parser.parse_args()

    root = Path(args.directory)
    threshold = parse_size(args.min_size)
    cache = {}
    results = []

    for item in walk(root):
        if not item.exists() and not item.is_symlink():
            continue
        if not matches_type(item, args.type):
            continue
        size = size_of_path(item, cache)
        if size >= threshold:
            results.append((size, item))

    results.sort(key=lambda pair: pair[0], reverse=True)
    if args.top is not None:
        results = results[:args.top]

    total_size = sum(size for size, _ in results)

    for size, path in results:
        print(f"{path} ({human_size(size)})")

    print(f"Total: {len(results)} archivos, {human_size(total_size)}")


if __name__ == "__main__":
    main()