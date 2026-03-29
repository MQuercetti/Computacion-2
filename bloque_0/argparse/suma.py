#1.2
import sys

if len(sys.argv) < 2:
    print("Uso: python suma.py <numero1> [numero2] ...")
    sys.exit(1)

numeros = []
for valor in sys.argv[1:]:
    try:
        numeros.append(float(valor.replace(",", ".")))
    except ValueError:
        print(f"Error: '{valor}' no es un número válido")
        sys.exit(1)

total = sum(numeros)
print(f"La suma es: {total}")
