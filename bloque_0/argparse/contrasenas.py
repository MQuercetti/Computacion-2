import argparse
import secrets
import string

LETTERS = string.ascii_letters
NUMBERS = string.digits
SYMBOLS = "!@#$%&"


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("debe ser un entero mayor a 0")
    return number


def build_pool(exclude_symbols, exclude_numbers):
    pool = LETTERS

    if not exclude_numbers:
        pool += NUMBERS

    if not exclude_symbols:
        pool += SYMBOLS

    return pool


def generate_password(length, pool):
    return "".join(secrets.choice(pool) for _ in range(length))


def main():
    parser = argparse.ArgumentParser(
        description="Generador de contraseñas seguras"
    )
    parser.add_argument(
        "-n",
        "--length",
        type=positive_int,
        default=12,
        help="Longitud de cada contraseña (default: 12)",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Excluye símbolos especiales (!@#$%%&)",
    )
    parser.add_argument(
        "--no-numbers",
        action="store_true",
        help="Excluye números",
    )
    parser.add_argument(
        "--count",
        type=positive_int,
        default=1,
        help="Cantidad de contraseñas a generar (default: 1)",
    )

    args = parser.parse_args()

    pool = build_pool(args.no_symbols, args.no_numbers)

    for _ in range(args.count):
        print(generate_password(args.length, pool))


if __name__ == "__main__":
    main()
