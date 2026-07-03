#!/usr/bin/env python3

import argparse
import grp
import os
import pwd
import stat
import sys
from pathlib import Path


def human_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    unit = units[0]
    for candidate in units:
        unit = candidate
        if value < 1024 or candidate == units[-1]:
            break
        value /= 1024
    if unit == "B":
        return f"{int(value)} bytes"
    return f"{value:.2f} {unit}"


def permissions_text(mode):
    symbols = []
    for mask, char in ((stat.S_IRUSR, "r"), (stat.S_IWUSR, "w"), (stat.S_IXUSR, "x"),
                       (stat.S_IRGRP, "r"), (stat.S_IWGRP, "w"), (stat.S_IXGRP, "x"),
                       (stat.S_IROTH, "r"), (stat.S_IWOTH, "w"), (stat.S_IXOTH, "x")):
        symbols.append(char if mode & mask else "-")
    return "".join(symbols)


def file_type(mode, path):
    if stat.S_ISLNK(mode):
        return f"enlace simbólico -> {os.readlink(path)}"
    if stat.S_ISDIR(mode):
        return "directorio"
    if stat.S_ISREG(mode):
        return "archivo regular"
    if stat.S_ISCHR(mode):
        return "dispositivo de caracteres"
    if stat.S_ISBLK(mode):
        return "dispositivo de bloques"
    if stat.S_ISFIFO(mode):
        return "fifo"
    if stat.S_ISSOCK(mode):
        return "socket"
    return "desconocido"


def owner_name(uid):
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return str(uid)


def group_name(gid):
    try:
        return grp.getgrgid(gid).gr_name
    except KeyError:
        return str(gid)


def inspect(path_text):
    path = Path(path_text)
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        print(f"Error: no existe '{path_text}'", file=sys.stderr)
        sys.exit(1)
    except OSError as error:
        print(f"Error: no se puede inspeccionar '{path_text}': {error}", file=sys.stderr)
        sys.exit(1)

    mode = info.st_mode
    perms = permissions_text(mode)
    octal = oct(stat.S_IMODE(mode))[2:]

    print(f"Archivo: {path_text}")
    print(f"Tipo: {file_type(mode, path_text)}")
    print(f"Tamaño: {info.st_size} bytes ({human_size(info.st_size)})")
    print(f"Permisos: {perms} ({octal})")
    print(f"Propietario: {owner_name(info.st_uid)} (uid: {info.st_uid})")
    print(f"Grupo: {group_name(info.st_gid)} (gid: {info.st_gid})")
    print(f"Inodo: {info.st_ino}")
    print(f"Enlaces duros: {info.st_nlink}")
    print(f"Último acceso: {time_text(info.st_atime)}")
    print(f"Última modificación: {time_text(info.st_mtime)}")
    print(f"Cambio de metadatos: {time_text(info.st_ctime)}")

    if stat.S_ISDIR(mode):
        try:
            count = sum(1 for _ in path.iterdir())
        except OSError as error:
            print(f"Contenido: error al contar elementos ({error})")
        else:
            print(f"Contenido: {count} elementos")


def time_text(timestamp):
    from datetime import datetime

    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="Inspector detallado de archivos y directorios")
    parser.add_argument("path", help="Ruta a inspeccionar")
    args = parser.parse_args()
    inspect(args.path)


if __name__ == "__main__":
    main()