import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Version simplificada de grep")
    parser.add_argument("patron", help="Patron a buscar")
    parser.add_argument("archivos", nargs="*", help="Archivos de entrada")
    parser.add_argument(
        "-i",
        "--ignore-case",
        action="store_true",
        help="Busqueda insensible a mayusculas",
    )
    parser.add_argument(
        "-n",
        "--line-number",
        action="store_true",
        help="Muestra numero de linea",
    )
    parser.add_argument(
        "-c",
        "--count",
        action="store_true",
        help="Muestra solo el conteo de coincidencias",
    )
    parser.add_argument(
        "-v",
        "--invert",
        action="store_true",
        help="Muestra lineas que no coinciden",
    )
    return parser.parse_args()


def normalize(text, ignore_case):
    if ignore_case:
        return text.lower()
    return text


def line_matches(line, pattern, ignore_case, invert):
    candidate = normalize(line, ignore_case)
    target = normalize(pattern, ignore_case)
    matched = target in candidate
    if invert:
        return not matched
    return matched


def process_stream(stream, pattern, args, file_label=None, show_file_label=False):
    matches = 0
    show_line_number = args.line_number or (len(args.archivos) > 1)

    for line_number, line in enumerate(stream, start=1):
        if not line_matches(line, pattern, args.ignore_case, args.invert):
            continue

        matches += 1
        if args.count:
            continue

        output = ""
        if show_file_label:
            output += f"{file_label}:"

        if show_line_number:
            output += f"{line_number}:"

        output += line
        if not output.endswith("\n"):
            output += "\n"

        print(output, end="")

    return matches


def main():
    args = parse_args()

    if not args.archivos:
        total = process_stream(sys.stdin, args.patron, args)
        if args.count:
            print(total)
        return

    show_file_label = len(args.archivos) > 1

    for file_name in args.archivos:
        try:
            with open(file_name, "r", encoding="utf-8") as input_file:
                total = process_stream(
                    input_file,
                    args.patron,
                    args,
                    file_label=file_name,
                    show_file_label=show_file_label,
                )

            if args.count:
                if show_file_label:
                    print(f"{file_name}:{total}")
                else:
                    print(total)
        except OSError as error:
            print(f"Error: No se puede leer '{file_name}': {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
