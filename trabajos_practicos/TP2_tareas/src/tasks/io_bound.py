import asyncio
import time
from typing import List, Dict, Any
import httpx


async def _descargar_una(client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
    """Descarga una URL individual midiendo tiempo, tamaño y status code."""
    inicio = time.perf_counter()
    try:
        response = await client.get(url, follow_redirects=True, timeout=15.0)
        duracion = time.perf_counter() - inicio
        return {
            "url": url,
            "status_code": response.status_code,
            "tamano_bytes": len(response.content),
            "tiempo_segundos": round(duracion, 4),
            "exito": response.is_success
        }
    except httpx.RequestError as e:
        duracion = time.perf_counter() - inicio
        return {
            "url": url,
            "status_code": None,
            "tamano_bytes": 0,
            "tiempo_segundos": round(duracion, 4),
            "exito": False,
            "error": str(e)
        }


async def ejecutar_descargas(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Descarga una lista de URLs concurrentemente mediante httpx y asyncio.gather.
    
    Aprovecha la naturaleza I/O-bound: N descargas se realizan en paralelo
    sobre el event loop sin bloquear el hilo principal.
    """
    async with httpx.AsyncClient() as client:
        tareas = [_descargar_una(client, url) for url in urls]
        # asyncio.gather ejecuta todas las corrutinas concurrentemente
        resultados = await asyncio.gather(*tareas, return_exceptions=False)
        return list(resultados)
