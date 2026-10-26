import asyncio
import time
from typing import Dict, Any


async def ejecutar_espera(segundos: float) -> Dict[str, Any]:
    """
    Tarea de I/O simulado mediante asyncio.sleep.
    
    Permite validar:
    1. Que el event loop sigue atendiendo otras tareas y peticiones HTTP.
    2. Cancelación limpia en pleno vuelo al disparar DELETE /tareas/{id}.
    3. Expiración controlada por timeout.
    """
    inicio = time.perf_counter()
    await asyncio.sleep(segundos)
    fin = time.perf_counter()
    return {
        "segundos_solicitados": segundos,
        "segundos_reales": round(fin - inicio, 4),
        "mensaje": "Espera finalizada exitosamente"
    }
