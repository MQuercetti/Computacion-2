import hashlib
import time


def compute_iterative_hash(texto: str, iteraciones: int) -> dict:
    """
    Función intensiva en CPU que calcula SHA-256 de forma iterativa.
    
    Está definida como función top-level pura para poder ser ejecutada
    directamente en un ProcessPoolExecutor mediante serialización con pickle
    tanto en Linux (fork) como en Windows/macOS (spawn).
    """
    inicio = time.perf_counter()
    data = texto.encode("utf-8")
    for _ in range(iteraciones):
        data = hashlib.sha256(data).digest()
    
    fin = time.perf_counter()
    return {
        "hash_final": data.hex(),
        "iteraciones": iteraciones,
        "tiempo_calculo_segundos": round(fin - inicio, 4)
    }
