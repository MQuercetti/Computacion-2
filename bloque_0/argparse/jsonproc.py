import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Procesador simple de JSON")
    parser.add_argument(
        "archivo",
        help="Archivo JSON de entrada o '-' para leer desde stdin",
    )
    parser.add_argument(
        "--keys",
        action="store_true",
        help="Lista las claves del primer nivel",
    )
    parser.add_argument(
        "--get",
        metavar="KEY",
        help="Obtiene un valor con notacion de puntos (ej: usuario.nombre)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Imprime JSON con indentacion",
    )
    parser.add_argument(
        "--set",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Modifica un valor usando notacion de puntos",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        help="Archivo de salida (default: stdout)",
    )
    return parser.parse_args()


def parse_path(path):
    if not path:
        return []
    return path.split(".")


def token_to_index(token):
    try:
        return int(token)
    except ValueError:
        return None


def parse_value(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def load_json(source):
    try:
        if source == "-":
            return json.load(sys.stdin)

        with open(source, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: no existe el archivo '{source}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as error:
        print(f"Error: JSON invalido: {error}", file=sys.stderr)
        sys.exit(1)
    except OSError as error:
        print(f"Error: no se puede leer '{source}': {error}", file=sys.stderr)
        sys.exit(1)


def resolve_path(data, path):
    current = data
    for token in parse_path(path):
        index = token_to_index(token)

        if isinstance(current, list):
            if index is None:
                raise KeyError(f"Se esperaba indice numerico, se recibio '{token}'")
            if index < 0 or index >= len(current):
                raise KeyError(f"Indice fuera de rango: {index}")
            current = current[index]
            continue

        if isinstance(current, dict):
            if token not in current:
                raise KeyError(f"Clave inexistente: {token}")
            current = current[token]
            continue

        raise KeyError(f"No se puede navegar sobre tipo {type(current).__name__}")

    return current


def set_path(data, path, value):
    tokens = parse_path(path)
    if not tokens:
        raise KeyError("La ruta no puede estar vacia")

    current = data

    for token in tokens[:-1]:
        index = token_to_index(token)

        if isinstance(current, list):
            if index is None:
                raise KeyError(f"Se esperaba indice numerico, se recibio '{token}'")
            if index < 0 or index >= len(current):
                raise KeyError(f"Indice fuera de rango: {index}")
            current = current[index]
            continue

        if isinstance(current, dict):
            if token not in current:
                raise KeyError(f"Clave inexistente: {token}")
            current = current[token]
            continue

        raise KeyError(f"No se puede navegar sobre tipo {type(current).__name__}")

    last = tokens[-1]
    last_index = token_to_index(last)

    if isinstance(current, list):
        if last_index is None:
            raise KeyError(f"Se esperaba indice numerico final, se recibio '{last}'")
        if last_index < 0 or last_index >= len(current):
            raise KeyError(f"Indice fuera de rango: {last_index}")
        current[last_index] = value
        return

    if isinstance(current, dict):
        current[last] = value
        return

    raise KeyError(f"No se puede asignar sobre tipo {type(current).__name__}")


def format_json(value, pretty):
    if pretty:
        return json.dumps(value, ensure_ascii=False, indent=2)
    return json.dumps(value, ensure_ascii=False)


def write_output(text, destination):
    if destination == "-":
        print(text)
        return

    try:
        with open(destination, "w", encoding="utf-8") as file:
            file.write(text)
            if not text.endswith("\n"):
                file.write("\n")
    except OSError as error:
        print(f"Error: no se puede escribir en '{destination}': {error}", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_args()
    data = load_json(args.archivo)

    if args.set:
        path, raw_value = args.set
        value = parse_value(raw_value)
        try:
            set_path(data, path, value)
        except KeyError as error:
            print(f"Error: ruta invalida para --set: {error}", file=sys.stderr)
            sys.exit(1)

    if args.keys:
        if not isinstance(data, dict):
            print("Error: --keys requiere un JSON objeto en el nivel superior", file=sys.stderr)
            sys.exit(1)
        result = "\n".join(sorted(data.keys()))
        write_output(result, args.output)
        return

    if args.get:
        try:
            value = resolve_path(data, args.get)
        except KeyError as error:
            print(f"Error: ruta invalida para --get: {error}", file=sys.stderr)
            sys.exit(1)
        write_output(format_json(value, args.pretty), args.output)
        return

    write_output(format_json(data, args.pretty), args.output)


if __name__ == "__main__":
    main()
