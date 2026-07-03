import argparse


def format_input_temperature(value):
    if float(value).is_integer():
        return str(int(value))
    return f"{value}"


def format_output_temperature(value):
    if float(value).is_integer():
        return f"{value:.1f}"

    text = f"{value:.2f}".rstrip("0").rstrip(".")
    if "." not in text:
        text += ".0"
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Convierte temperaturas entre Celsius y Fahrenheit"
    )
    parser.add_argument(
        "valor",
        type=float,
        help="Valor numerico decimal a convertir",
    )
    parser.add_argument(
        "-t",
        "--to",
        required=True,
        choices=["celsius", "fahrenheit"],
        help="Unidad de destino",
    )

    args = parser.parse_args()

    if args.to == "celsius":
        resultado = (args.valor - 32) * 5 / 9
        print(f"{format_input_temperature(args.valor)}°F = {format_output_temperature(resultado)}°C")
    else:
        resultado = (args.valor * 9 / 5) + 32
        print(f"{format_input_temperature(args.valor)}°C = {format_output_temperature(resultado)}°F")


if __name__ == "__main__":
    main()
