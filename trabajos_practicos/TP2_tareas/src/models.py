from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, Field, HttpUrl, model_validator


class EstadoTarea(str, Enum):
    PENDIENTE = "pendiente"
    EJECUTANDO = "ejecutando"
    COMPLETADA = "completada"
    FALLIDA = "fallida"
    CANCELADA = "cancelada"


class TipoTarea(str, Enum):
    DESCARGAR = "descargar"
    HASHEAR = "hashear"
    ESPERAR = "esperar"


class CrearTareaRequest(BaseModel):
    tipo: TipoTarea = Field(..., description="Tipo de tarea a ejecutar")
    
    # Parámetros para 'descargar'
    urls: Optional[List[str]] = Field(None, description="Lista de URLs a descargar concurrentemente")
    
    # Parámetros para 'hashear'
    texto: Optional[str] = Field(None, description="Texto de entrada a hashear intensivamente")
    iteraciones: Optional[int] = Field(None, ge=1, description="Cantidad de iteraciones de SHA-256")
    
    # Parámetros para 'esperar'
    segundos: Optional[float] = Field(None, ge=0.0, description="Cantidad de segundos a dormir asíncronamente")
    
    # Configuración de timeout
    timeout: Optional[float] = Field(None, gt=0.0, description="Timeout específico en segundos para esta tarea")

    @model_validator(mode="after")
    def validar_parametros_por_tipo(self) -> "CrearTareaRequest":
        if self.tipo == TipoTarea.DESCARGAR:
            if not self.urls or len(self.urls) == 0:
                raise ValueError("Para la tarea 'descargar' se requiere una lista de 'urls' no vacía.")
        elif self.tipo == TipoTarea.HASHEAR:
            if self.texto is None:
                raise ValueError("Para la tarea 'hashear' se requiere el campo 'texto'.")
            if not self.iteraciones or self.iteraciones < 1:
                raise ValueError("Para la tarea 'hashear' se requiere 'iteraciones' mayor o igual a 1.")
        elif self.tipo == TipoTarea.ESPERAR:
            if self.segundos is None or self.segundos < 0:
                raise ValueError("Para la tarea 'esperar' se requiere 'segundos' mayor o igual a 0.")
        return self


class TareaResponse(BaseModel):
    id: str = Field(..., description="Identificador único UUID de la tarea")
    tipo: TipoTarea = Field(..., description="Tipo de la tarea")
    estado: EstadoTarea = Field(..., description="Estado actual de la tarea")
    creada_en: str = Field(..., description="Timestamp ISO de creación/encolado")
    iniciada_en: Optional[str] = Field(None, description="Timestamp ISO de inicio de procesamiento")
    finalizada_en: Optional[str] = Field(None, description="Timestamp ISO de finalización")
    duracion_segundos: Optional[float] = Field(None, description="Duración efectiva de la ejecución en segundos")
    resultado: Optional[Any] = Field(None, description="Datos de resultado si la tarea se completó con éxito")
    error: Optional[str] = Field(None, description="Mensaje de error o motivo de fallo/timeout")


class EstadisticasResponse(BaseModel):
    total_tareas: int
    por_estado: dict[str, int]
    workers_totales: int
    workers_ocupados: int
    tiempo_promedio_ejecucion_segundos: Optional[float] = None
