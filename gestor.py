import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from models import TareaBase, TareaSimple, TareaPrioritaria, TareaConFecha, EstadoTarea, PrioridadTarea

class GestorTareas:
    """
    ENCAPSULACIÓN: Gestiona una colección privada de tareas
    ABSTRACCIÓN: Proporciona una interfaz simple para operaciones CRUD
    """
    
    def __init__(self):
        # ENCAPSULACIÓN: Lista privada de tareas
        self._tareas: Dict[int, TareaBase] = {}
        self._siguiente_id = 1
        self.cargar_tareas()

    def _generar_id(self) -> int:
        """Método privado para generar IDs únicos"""
        id_actual = self._siguiente_id
        self._siguiente_id += 1
        return id_actual
    
    # POLIMORFISMO: Método que acepta diferentes tipos de tareas
    def crear_tarea(self, tipo: str, titulo: str, descripcion: str = "", **kwargs) -> TareaBase:
        """
        Crea una tarea según el tipo especificado
        POLIMORFISMO: Maneja diferentes tipos de tareas de forma uniforme
        """
        if not titulo.strip():
            raise ValueError("El título no puede estar vacío")
        
        id_tarea = self._generar_id()
        
        # Factory pattern simple para crear diferentes tipos de tareas
        if tipo.lower() == "simple":
            tarea = TareaSimple(id_tarea, titulo, descripcion)
        elif tipo.lower() == "prioritaria":
            prioridad_str = kwargs.get("prioridad", "media")
            try:
                prioridad = PrioridadTarea(prioridad_str)
            except ValueError:
                prioridad = PrioridadTarea.MEDIA
            tarea = TareaPrioritaria(id_tarea, titulo, descripcion, prioridad)
        elif tipo.lower() == "con_fecha":
            fecha_limite = kwargs.get("fecha_limite")
            if isinstance(fecha_limite, str):
                try:
                    fecha_limite = datetime.fromisoformat(fecha_limite)
                except ValueError:
                    fecha_limite = None
            tarea = TareaConFecha(id_tarea, titulo, descripcion, fecha_limite)
        else:
            # Por defecto, crear tarea simple
            tarea = TareaSimple(id_tarea, titulo, descripcion)
        
        self._tareas[id_tarea] = tarea
        self.guardar_tareas()
        return tarea
    
    def obtener_tarea(self, id_tarea: int) -> Optional[TareaBase]:
        """Obtiene una tarea por su ID"""
        return self._tareas.get(id_tarea)
    
    def listar_tareas(self, estado: Optional[str] = None) -> List[TareaBase]:
        """
        Lista todas las tareas o filtradas por estado
        POLIMORFISMO: Maneja diferentes tipos de tareas uniformemente
        """
        tareas = list(self._tareas.values())
        
        if estado:
            try:
                estado_enum = EstadoTarea(estado)
                tareas = [t for t in tareas if t.estado == estado_enum]
            except ValueError:
                pass  # Si el estado no es válido, devolver todas
        
        return tareas
    
    def actualizar_tarea(self, id_tarea: int, **kwargs) -> Optional[TareaBase]:
        """
        Actualiza una tarea existente
        POLIMORFISMO: Maneja diferentes tipos de tareas
        """
        tarea = self._tareas.get(id_tarea)
        if not tarea:
            return None
        
        # Actualizar campos comunes
        if "titulo" in kwargs:
            tarea.titulo = kwargs["titulo"]
        if "descripcion" in kwargs:
            tarea.descripcion = kwargs["descripcion"]
        if "estado" in kwargs:
            try:
                tarea.estado = EstadoTarea(kwargs["estado"])
            except ValueError:
                pass  # Ignorar estados inválidos
        
        # Actualizar campos específicos según el tipo de tarea
        if isinstance(tarea, TareaPrioritaria) and "prioridad" in kwargs:
            try:
                tarea.prioridad = PrioridadTarea(kwargs["prioridad"])
            except ValueError:
                pass
        
        if isinstance(tarea, TareaConFecha) and "fecha_limite" in kwargs:
            fecha = kwargs["fecha_limite"]
            if isinstance(fecha, str):
                try:
                    fecha = datetime.fromisoformat(fecha)
                except ValueError:
                    fecha = None
            tarea.fecha_limite = fecha
        
        self.guardar_tareas()
        return tarea
    
    def eliminar_tarea(self, id_tarea: int) -> bool:
        """Elimina una tarea por su ID"""
        if id_tarea in self._tareas:
            del self._tareas[id_tarea]
            self.guardar_tareas()
            return True
        return False
    
    def marcar_completada(self, id_tarea: int) -> Optional[TareaBase]:
        """
        Marca una tarea como completada
        POLIMORFISMO: Utiliza el método específico de cada tipo de tarea
        """
        tarea = self._tareas.get(id_tarea)
        if tarea:
            tarea.marcar_completada()  # Polimorfismo en acción
            self.guardar_tareas()
            return tarea
        return None
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas básicas de las tareas"""
        total = len(self._tareas)
        if total == 0:
            return {"total": 0, "pendientes": 0, "en_progreso": 0, "completadas": 0}
        
        pendientes = sum(1 for t in self._tareas.values() if t.estado == EstadoTarea.PENDIENTE)
        en_progreso = sum(1 for t in self._tareas.values() if t.estado == EstadoTarea.EN_PROGRESO)
        completadas = sum(1 for t in self._tareas.values() if t.estado == EstadoTarea.COMPLETADA)
        
        return {
            "total": total,
            "pendientes": pendientes,
            "en_progreso": en_progreso,
            "completadas": completadas
        }
    
    def obtener_tareas_vencidas(self) -> List[TareaBase]:
        """Obtiene tareas con fecha límite vencida"""
        tareas_vencidas = []
        for tarea in self._tareas.values():
            if isinstance(tarea, TareaConFecha) and tarea.esta_vencida():
                tareas_vencidas.append(tarea)
        return tareas_vencidas

    def guardar_tareas(self):
        """Guardar tareas en un archivo JSON"""
        with open("tareas.json", "w") as file:
            tareas_data = {id_tarea: tarea.to_dict() for id_tarea, tarea in self._tareas.items()}
            json.dump(tareas_data, file, indent=4)

    def cargar_tareas(self):
        """Cargar tareas desde un archivo JSON"""
        try:
            with open("tareas.json", "r") as file:
                tareas_data = json.load(file)
                for id_tarea, tarea_data in tareas_data.items():
                    tarea_data["id"] = int(id_tarea)
                    if tarea_data["tipo"] == "TareaSimple":
                        tarea = TareaSimple(**tarea_data)
                    elif tarea_data["tipo"] == "TareaPrioritaria":
                        tarea = TareaPrioritaria(**tarea_data)
                    elif tarea_data["tipo"] == "TareaConFecha":
                        tarea = TareaConFecha(**tarea_data)
                    self._tareas[tarea.id] = tarea
                    self._siguiente_id = max(self._siguiente_id, tarea.id + 1)
        except FileNotFoundError:
            pass