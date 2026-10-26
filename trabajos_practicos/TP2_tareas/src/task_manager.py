import asyncio
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import time
from typing import Dict, List, Optional
import uuid

from .config import DEFAULT_TASK_TIMEOUT, DUMP_DIR, SHUTDOWN_TIMEOUT, WORKER_COUNT
from .models import (
    CrearTareaRequest,
    EstadoTarea,
    EstadisticasResponse,
    TareaResponse,
    TipoTarea,
)
from .tasks.cpu_bound import compute_iterative_hash
from .tasks.io_bound import ejecutar_descargas
from .tasks.simulated import ejecutar_espera

logger = logging.getLogger("task_manager")


class TaskManager:
    """
    Gestor central de tareas asíncronas, cola de trabajo y pool de workers.
    
    Responsabilidades:
    - Almacenar tareas en memoria con estados coherentes.
    - Administrar una asyncio.Queue compartida para el patrón productor-consumidor.
    - Mantener un pool de N workers corrutinas activos.
    - Ejecutar tareas CPU-bound en un ProcessPoolExecutor sin bloquear el event loop.
    - Cancelar tareas encoladas y en ejecución sin fugas de corrutinas.
    - Volcar estado en JSON durante el apagado ordenado (graceful shutdown).
    """

    def __init__(
        self,
        worker_count: int = WORKER_COUNT,
        default_timeout: float = DEFAULT_TASK_TIMEOUT,
        dump_dir: Path = DUMP_DIR,
    ):
        self.worker_count = worker_count
        self.default_timeout = default_timeout
        self.dump_dir = dump_dir
        
        # Diccionario en memoria: id -> TareaResponse (o dict)
        self.tareas: Dict[str, dict] = {}
        
        # Cola asíncrona de IDs de tareas a procesar
        self.cola: asyncio.Queue[str] = asyncio.Queue()
        
        # Control de asyncio.Task en curso para permitir cancelación
        self._tareas_en_vuelo: Dict[str, asyncio.Task] = {}
        
        # Control de workers corrutinas
        self._workers: List[asyncio.Task] = []
        self._workers_ocupados: int = 0
        self._running: bool = False
        
        # Executor de procesos para CPU-bound
        self._process_pool: Optional[ProcessPoolExecutor] = None

    async def start(self) -> None:
        """Inicializa los workers y el ProcessPoolExecutor."""
        if self._running:
            return
        
        self._running = True
        self.cola = asyncio.Queue()
        self._process_pool = ProcessPoolExecutor()
        
        # Revisar si existen volcados previos para loguear
        self._reportar_volcados_previos()
        
        # Iniciar los N workers
        for worker_id in range(self.worker_count):
            task = asyncio.create_task(
                self._worker_loop(worker_id),
                name=f"worker-{worker_id}"
            )
            self._workers.append(task)
        
        logger.info(
            f"TaskManager iniciado con {self.worker_count} workers y ProcessPoolExecutor listo."
        )

    def _reportar_volcados_previos(self) -> None:
        try:
            volcados = sorted(self.dump_dir.glob("estado_*.json"))
            if volcados:
                ultimo = volcados[-1]
                logger.info(
                    f"Se encontró volcado de estado previo: {ultimo.name} "
                    f"(Total encontrados: {len(volcados)})"
                )
        except Exception as e:
            logger.warning(f"No se pudieron verificar volcados previos: {e}")

    async def stop(self, timeout: float = SHUTDOWN_TIMEOUT) -> str:
        """
        Apagado ordenado (graceful shutdown):
        1. Marca el gestor como detenido (no se procesan más ítems nuevos).
        2. Espera a que las tareas en curso terminen hasta un tiempo límite.
        3. Cancela workers y cierra el executor de procesos.
        4. Vuelca el estado completo a un archivo JSON.
        """
        logger.info("Iniciando apagado ordenado del TaskManager...")
        self._running = False
        
        # Esperar tareas en vuelo activas
        en_vuelo = list(self._tareas_en_vuelo.values())
        if en_vuelo:
            logger.info(
                f"Esperando finalización de {len(en_vuelo)} tareas en curso (timeout {timeout}s)..."
            )
            done, pending = await asyncio.wait(en_vuelo, timeout=timeout)
            for p in pending:
                p.cancel()
        
        # Cancelar workers corrutinas
        for worker in self._workers:
            worker.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        
        # Apagar pool de procesos
        if self._process_pool:
            self._process_pool.shutdown(wait=False, cancel_futures=True)
            self._process_pool = None

        # Volcado de estado a JSON
        dump_path = self._volcar_estado_a_disco()
        logger.info(f"Apagado completado. Estado volcado a {dump_path}")
        return dump_path

    def _volcar_estado_a_disco(self) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"estado_{timestamp}.json"
        target = self.dump_dir / filename
        
        # Serializar tareas
        serializable_data = {
            "fecha_volcado": datetime.now(timezone.utc).isoformat(),
            "total_tareas": len(self.tareas),
            "tareas": self.tareas,
        }
        with open(target, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        return str(target)

    async def encolar_tarea(self, req: CrearTareaRequest) -> TareaResponse:
        """Encola una nueva tarea en la cola asíncrona y devuelve su respuesta inmediata."""
        if not self._running:
            raise RuntimeError("El gestor de tareas está detenido o apagándose.")

        tarea_id = str(uuid.uuid4())
        ahora = datetime.now(timezone.utc).isoformat()
        
        info_tarea = {
            "id": tarea_id,
            "tipo": req.tipo.value,
            "estado": EstadoTarea.PENDIENTE.value,
            "creada_en": ahora,
            "iniciada_en": None,
            "finalizada_en": None,
            "duracion_segundos": None,
            "resultado": None,
            "error": None,
            "params": req.model_dump(),
            "timeout": req.timeout or self.default_timeout,
        }
        
        self.tareas[tarea_id] = info_tarea
        await self.cola.put(tarea_id)
        logger.info(f"Tarea encolada: {tarea_id} (tipo={req.tipo.value})")
        return self._to_response(info_tarea)

    def obtener_tarea(self, tarea_id: str) -> Optional[TareaResponse]:
        info = self.tareas.get(tarea_id)
        if not info:
            return None
        return self._to_response(info)

    def listar_tareas(self, estado: Optional[EstadoTarea] = None) -> List[TareaResponse]:
        resultado = []
        for info in self.tareas.values():
            if estado is None or info["estado"] == estado.value:
                resultado.append(self._to_response(info))
        return resultado

    async def cancelar_tarea(self, tarea_id: str) -> Optional[TareaResponse]:
        """
        Cancela una tarea. Si está pendiente en la cola, la marca cancelada.
        Si está en ejecución, invoca cancel() sobre la asyncio.Task correspondiente.
        """
        info = self.tareas.get(tarea_id)
        if not info:
            return None

        estado_actual = info["estado"]
        if estado_actual in [EstadoTarea.COMPLETADA.value, EstadoTarea.FALLIDA.value, EstadoTarea.CANCELADA.value]:
            return self._to_response(info)

        if estado_actual == EstadoTarea.PENDIENTE.value:
            info["estado"] = EstadoTarea.CANCELADA.value
            info["finalizada_en"] = datetime.now(timezone.utc).isoformat()
            info["error"] = "Tarea cancelada por el usuario mientras estaba en cola"
            logger.info(f"Tarea {tarea_id} cancelada en estado pendiente.")
            return self._to_response(info)

        # Si está ejecutando
        tarea_task = self._tareas_en_vuelo.get(tarea_id)
        if tarea_task and not tarea_task.done():
            tarea_task.cancel()
            logger.info(f"Cancelación solicitada para tarea en ejecución: {tarea_id}")

        info["estado"] = EstadoTarea.CANCELADA.value
        info["finalizada_en"] = datetime.now(timezone.utc).isoformat()
        info["error"] = "Tarea cancelada por el usuario durante su ejecución"
        return self._to_response(info)

    def obtener_estadisticas(self) -> EstadisticasResponse:
        conteos = {estado.value: 0 for estado in EstadoTarea}
        duraciones = []
        
        for t in self.tareas.values():
            st = t["estado"]
            conteos[st] = conteos.get(st, 0) + 1
            if t.get("duracion_segundos") is not None:
                duraciones.append(t["duracion_segundos"])
        
        promedio = (sum(duraciones) / len(duraciones)) if duraciones else None
        
        return EstadisticasResponse(
            total_tareas=len(self.tareas),
            por_estado=conteos,
            workers_totales=self.worker_count,
            workers_ocupados=self._workers_ocupados,
            tiempo_promedio_ejecucion_segundos=round(promedio, 4) if promedio is not None else None,
        )

    async def _worker_loop(self, worker_id: int) -> None:
        """Loop principal de cada worker corrutina consumiendo de la cola compartida."""
        logger.debug(f"Worker {worker_id} listo para procesar tareas.")
        while self._running:
            try:
                tarea_id = await self.cola.get()
            except asyncio.CancelledError:
                break
            
            info = self.tareas.get(tarea_id)
            if not info:
                self.cola.task_done()
                continue
            
            # Si fue cancelada mientras esperaba en la cola
            if info["estado"] == EstadoTarea.CANCELADA.value:
                self.cola.task_done()
                continue

            self._workers_ocupados += 1
            info["estado"] = EstadoTarea.EJECUTANDO.value
            info["iniciada_en"] = datetime.now(timezone.utc).isoformat()
            
            # Crear asyncio.Task para envolver la ejecución con timeout y permitir cancelación
            loop = asyncio.get_running_loop()
            task_ejecucion = asyncio.create_task(
                self._ejecutar_con_timeout(info),
                name=f"task-exec-{tarea_id}"
            )
            self._tareas_en_vuelo[tarea_id] = task_ejecucion

            try:
                await task_ejecucion
            except asyncio.CancelledError:
                # Cancelación limpia: solo marcar cancelada si no fue marcada previamente
                if info["estado"] != EstadoTarea.CANCELADA.value:
                    info["estado"] = EstadoTarea.CANCELADA.value
                    info["finalizada_en"] = datetime.now(timezone.utc).isoformat()
                    info["error"] = info.get("error") or "Tarea cancelada"
            except Exception as e:
                # Blindaje ante cualquier excepción imprevista
                logger.exception(f"Error inesperado en worker {worker_id} al procesar {tarea_id}: {e}")
                info["estado"] = EstadoTarea.FALLIDA.value
                info["finalizada_en"] = datetime.now(timezone.utc).isoformat()
                info["error"] = f"Error no capturado: {str(e)}"
            finally:
                self._tareas_en_vuelo.pop(tarea_id, None)
                self._workers_ocupados -= 1
                self.cola.task_done()

    async def _ejecutar_con_timeout(self, info: dict) -> None:
        """Aplica el timeout configurado a la ejecución de la tarea."""
        timeout_segundos = info.get("timeout") or self.default_timeout
        inicio = time.perf_counter()
        
        try:
            resultado = await asyncio.wait_for(
                self._despachar_tarea(info),
                timeout=timeout_segundos
            )
            duracion = time.perf_counter() - inicio
            info["estado"] = EstadoTarea.COMPLETADA.value
            info["resultado"] = resultado
            info["duracion_segundos"] = round(duracion, 4)
            info["finalizada_en"] = datetime.now(timezone.utc).isoformat()
        except asyncio.TimeoutError:
            duracion = time.perf_counter() - inicio
            info["estado"] = EstadoTarea.FALLIDA.value
            info["duracion_segundos"] = round(duracion, 4)
            info["finalizada_en"] = datetime.now(timezone.utc).isoformat()
            info["error"] = f"Timeout excedido: la tarea superó el límite de {timeout_segundos}s"
            logger.warning(f"Tarea {info['id']} finalizó por timeout ({timeout_segundos}s).")
        except asyncio.CancelledError:
            duracion = time.perf_counter() - inicio
            info["duracion_segundos"] = round(duracion, 4)
            raise

    async def _despachar_tarea(self, info: dict) -> dict:
        """Despacha la tarea según su tipo a la función o executor correspondiente."""
        tipo = info["tipo"]
        params = info["params"]

        if tipo == TipoTarea.DESCARGAR.value:
            urls = params.get("urls", [])
            return {"descargas": await ejecutar_descargas(urls)}

        elif tipo == TipoTarea.HASHEAR.value:
            texto = params.get("texto", "")
            iteraciones = params.get("iteraciones", 1000)
            
            # Ejecución CPU-bound en ProcessPoolExecutor para no bloquear el event loop
            loop = asyncio.get_running_loop()
            resultado = await loop.run_in_executor(
                self._process_pool,
                compute_iterative_hash,
                texto,
                iteraciones
            )
            return resultado

        elif tipo == TipoTarea.ESPERAR.value:
            segundos = params.get("segundos", 1.0)
            return await ejecutar_espera(segundos)

        else:
            raise ValueError(f"Tipo de tarea desconocido: {tipo}")

    def _to_response(self, info: dict) -> TareaResponse:
        return TareaResponse(
            id=info["id"],
            tipo=TipoTarea(info["tipo"]),
            estado=EstadoTarea(info["estado"]),
            creada_en=info["creada_en"],
            iniciada_en=info.get("iniciada_en"),
            finalizada_en=info.get("finalizada_en"),
            duracion_segundos=info.get("duracion_segundos"),
            resultado=info.get("resultado"),
            error=info.get("error"),
        )
