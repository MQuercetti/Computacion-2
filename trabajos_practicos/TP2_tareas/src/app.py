from contextlib import asynccontextmanager
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, status

from .models import (
    CrearTareaRequest,
    EstadoTarea,
    EstadisticasResponse,
    TareaResponse,
)
from .task_manager import TaskManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("api")

# Instancia global del TaskManager
manager = TaskManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager de ciclo de vida de FastAPI.
    Inicia los workers y el pool de procesos al arrancar,
    y ejecuta el apagado ordenado al detenerse.
    """
    logger.info("Iniciando aplicación y workers asíncronos...")
    await manager.start()
    yield
    logger.info("Deteniendo aplicación y volcando estado...")
    await manager.stop()


app = FastAPI(
    title="Plataforma de Tareas Distribuidas",
    description="API HTTP asíncrona para encolado, ejecución concurrente y monitoreo de tareas",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post(
    "/tareas",
    response_model=TareaResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Encolar una nueva tarea",
    description="Encola una tarea y responde inmediatamente sin esperar su finalización.",
)
async def crear_tarea(request: CrearTareaRequest):
    try:
        tarea = await manager.encolar_tarea(request)
        return tarea
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )


@app.get(
    "/tareas",
    response_model=List[TareaResponse],
    summary="Listar tareas",
    description="Devuelve la lista de tareas en memoria con filtro opcional por estado.",
)
async def listar_tareas(
    estado: Optional[EstadoTarea] = Query(None, description="Filtrar por estado de tarea")
):
    return manager.listar_tareas(estado=estado)


@app.get(
    "/tareas/{tarea_id}",
    response_model=TareaResponse,
    summary="Consultar estado y resultado de una tarea",
)
async def obtener_tarea(tarea_id: str):
    tarea = manager.obtener_tarea(tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID '{tarea_id}' no encontrada.",
        )
    return tarea


@app.delete(
    "/tareas/{tarea_id}",
    response_model=TareaResponse,
    summary="Cancelar una tarea",
    description="Cancela una tarea que esté encolada (pendiente) o en ejecución.",
)
async def cancelar_tarea(tarea_id: str):
    tarea = await manager.cancelar_tarea(tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID '{tarea_id}' no encontrada.",
        )
    return tarea


@app.get(
    "/estadisticas",
    response_model=EstadisticasResponse,
    summary="Obtener métricas y estadísticas del sistema",
)
async def obtener_estadisticas():
    return manager.obtener_estadisticas()
