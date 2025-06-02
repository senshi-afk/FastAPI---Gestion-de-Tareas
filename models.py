from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from enum import Enum

class EstadoTarea(Enum):
    """Enum para definir estados de tareas"""
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"

class PrioridadTarea(Enum):
    """Enum para definir prioridades de tareas"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"

# ABSTRACCIÓN: Clase abstracta base
class TareaBase(ABC):
    """Clase abstracta base para todas las tareas"""
    def __init__(self, id: int, titulo: str, descripcion: str = ""):
        # ENCAPSULACIÓN: Atributos privados
        self._id = id
        self._titulo = titulo
        self._descripcion = descripcion
        self._fecha_creacion = datetime.now()
        self._estado = EstadoTarea.PENDIENTE
    
    # ENCAPSULACIÓN: Getters y setters
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def titulo(self) -> str:
        return self._titulo
    
    @titulo.setter
    def titulo(self, valor: str):
        if not valor.strip():
            raise ValueError("El título no puede estar vacío")
        self._titulo = valor
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, valor: str):
        self._descripcion = valor
    
    @property
    def estado(self) -> EstadoTarea:
        return self._estado
    
    @estado.setter
    def estado(self, valor: EstadoTarea):
        self._estado = valor
    
    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion
    
    # ABSTRACCIÓN: Método abstracto que debe implementar cada subclase
    @abstractmethod
    def obtener_info_especifica(self) -> str:
        pass
    
    # POLIMORFISMO: Método que puede ser sobrescrito
    def marcar_completada(self):
        self._estado = EstadoTarea.COMPLETADA
    
    def to_dict(self) -> dict:
        """Convierte la tarea a diccionario"""
        return {
            "id": self._id,
            "titulo": self._titulo,
            "descripcion": self._descripcion,
            "estado": self._estado.value,
            "fecha_creacion": self._fecha_creacion.isoformat(),
            "tipo": self.__class__.__name__,
            "info_especifica": self.obtener_info_especifica()
        }

# HERENCIA: Tarea simple hereda de TareaBase
class TareaSimple(TareaBase):
    def __init__(self, id: int, titulo: str, descripcion: str = ""):
        super().__init__(id, titulo, descripcion)
    
    # POLIMORFISMO: Implementación específica del método abstracto
    def obtener_info_especifica(self) -> str:
        return "Tarea simple sin características especiales"

# HERENCIA: Tarea con prioridad hereda de TareaBase
class TareaPrioritaria(TareaBase):
    def __init__(self, id: int, titulo: str, descripcion: str = "", prioridad: PrioridadTarea = PrioridadTarea.MEDIA):
        super().__init__(id, titulo, descripcion)
        self._prioridad = prioridad
    
    @property
    def prioridad(self) -> PrioridadTarea:
        return self._prioridad
    
    @prioridad.setter
    def prioridad(self, valor: PrioridadTarea):
        self._prioridad = valor
    
    # POLIMORFISMO: Implementación específica
    def obtener_info_especifica(self) -> str:
        return f"Prioridad: {self._prioridad.value}"
    
    # POLIMORFISMO: Sobrescribe el método padre
    def marcar_completada(self):
        super().marcar_completada()
        print(f"Tarea prioritaria '{self._titulo}' completada!")
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["prioridad"] = self._prioridad.value
        return data

# HERENCIA: Tarea con fecha límite hereda de TareaBase
class TareaConFecha(TareaBase):
    def __init__(self, id: int, titulo: str, descripcion: str = "", fecha_limite: Optional[datetime] = None):
        super().__init__(id, titulo, descripcion)
        self._fecha_limite = fecha_limite
    
    @property
    def fecha_limite(self) -> Optional[datetime]:
        return self._fecha_limite
    
    @fecha_limite.setter
    def fecha_limite(self, valor: Optional[datetime]):
        self._fecha_limite = valor
    
    # POLIMORFISMO: Implementación específica
    def obtener_info_especifica(self) -> str:
        if self._fecha_limite:
            return f"Fecha límite: {self._fecha_limite.strftime('%Y-%m-%d %H:%M')}"
        return "Sin fecha límite establecida"
    
    def esta_vencida(self) -> bool:
        if not self._fecha_limite:
            return False
        return datetime.now() > self._fecha_limite
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["fecha_limite"] = self._fecha_limite.isoformat() if self._fecha_limite else None
        data["vencida"] = self.esta_vencida()
        return data