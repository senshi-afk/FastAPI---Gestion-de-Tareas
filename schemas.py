from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums para validación
class EstadoTareaSchema(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completada = "completada"

class PrioridadTareaSchema(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"

class TipoTareaSchema(str, Enum):
    simple = "simple"
    prioritaria = "prioritaria"
    con_fecha = "con_fecha"

# Esquemas de entrada (Request)
class TareaCreate(BaseModel):
    tipo: TipoTareaSchema = Field(default=TipoTareaSchema.simple, description="Tipo de tarea")
    titulo: str = Field(..., min_length=1, max_length=200, description="Título de la tarea")
    descripcion: Optional[str] = Field(default="", max_length=1000, description="Descripción de la tarea")
    prioridad: Optional[PrioridadTareaSchema] = Field(default=None, description="Prioridad (solo para tareas prioritarias)")
    fecha_limite: Optional[datetime] = Field(default=None, description="Fecha límite (solo para tareas con fecha)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tipo": "simple",
                "titulo": "Completar proyecto",
                "descripcion": "Finalizar el desarrollo del API de tareas",
                "prioridad": "alta",
                "fecha_limite": "2024-12-31T23:59:59"
            }
        }

class TareaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=1000)
    estado: Optional[EstadoTareaSchema] = None
    prioridad: Optional[PrioridadTareaSchema] = None
    fecha_limite: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Nuevo título",
                "descripcion": "Nueva descripción",
                "estado": "en_progreso",
                "prioridad": "alta"
            }
        }

# Esquemas de salida (Response)
class TareaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    fecha_creacion: datetime
    tipo: str
    info_especifica: str
    prioridad: Optional[str] = None
    fecha_limite: Optional[datetime] = None
    vencida: Optional[bool] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "titulo": "Completar proyecto",
                "descripcion": "Finalizar el desarrollo del API de tareas",
                "estado": "pendiente",
                "fecha_creacion": "2024-01-15T10:30:00",
                "tipo": "TareaPrioritaria",
                "info_especifica": "Prioridad: alta",
                "prioridad": "alta",
                "fecha_limite": None,
                "vencida": None
            }
        }

class ListaTareasResponse(BaseModel):
    tareas: List[TareaResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "tareas": [],
                "total": 0
            }
        }

class EstadisticasResponse(BaseModel):
    total: int
    pendientes: int
    en_progreso: int
    completadas: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 10,
                "pendientes": 5,
                "en_progreso": 3,
                "completadas": 2
            }
        }

# Esquemas para respuestas de error
class ErrorResponse(BaseModel):
    error: str
    detalle: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Tarea no encontrada",
                "detalle": "No existe una tarea con el ID especificado"
            }
        }

# Esquema para respuestas exitosas
class MensajeResponse(BaseModel):
    mensaje: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Operación realizada exitosamente"
            }
        }