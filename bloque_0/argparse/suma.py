#1.2
import sys

numeros = []
has_decimal_input = False

for valor in sys.argv[1:]:
    try:
        if "." in valor or "," in valor:
            has_decimal_input = True
        numeros.append(float(valor.replace(",", ".")))
    except ValueError:
        print(f"Error: '{valor}' no es un número válido")
        sys.exit(1)

total = sum(numeros)
if total.is_integer() and not has_decimal_input:
    total = int(total)

print(f"Suma: {total}")
