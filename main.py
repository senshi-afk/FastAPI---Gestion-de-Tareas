from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from datetime import datetime

# Importar nuestras clases y esquemas
from models import TareaBase
from gestor import GestorTareas
from schemas import (
    TareaCreate, TareaUpdate, TareaResponse, ListaTareasResponse,
    EstadisticasResponse, ErrorResponse, MensajeResponse,
    EstadoTareaSchema
)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Gestor de Tareas",
    description="Una API simple para gestionar tareas aplicando principios de POO",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar Jinja2
templates = Jinja2Templates(directory="templates")

# Instancia global del gestor de tareas
gestor = GestorTareas()

def tarea_a_response(tarea: TareaBase) -> TareaResponse:
    """Convierte una tarea del modelo a schema de respuesta"""
    data = tarea.to_dict()
    return TareaResponse(**data)

# Ruta para la página principal con Jinja2
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para crear una nueva tarea
@app.post("/tareas", response_model=TareaResponse, status_code=201)
async def crear_tarea(tarea_data: TareaCreate):
    try:
        kwargs = {}
        if tarea_data.prioridad:
            kwargs["prioridad"] = tarea_data.prioridad.value
        if tarea_data.fecha_limite:
            kwargs["fecha_limite"] = tarea_data.fecha_limite
        
        tarea = gestor.crear_tarea(
            tipo=tarea_data.tipo.value,
            titulo=tarea_data.titulo,
            descripcion=tarea_data.descripcion,
            **kwargs
        )
        
        return tarea_a_response(tarea)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Ruta para listar todas las tareas
@app.get("/tareas", response_model=ListaTareasResponse)
async def listar_tareas(
    estado: Optional[EstadoTareaSchema] = Query(None, description="Filtrar por estado")
):
    try:
        estado_str = estado.value if estado else None
        tareas = gestor.listar_tareas(estado=estado_str)
        
        tareas_response = [tarea_a_response(t) for t in tareas]
        
        return ListaTareasResponse(
            tareas=tareas_response,
            total=len(tareas_response)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener las tareas")

# Ruta para obtener una tarea específica
@app.get("/tareas/{tarea_id}", response_model=TareaResponse)
async def obtener_tarea(tarea_id: int):
    tarea = gestor.obtener_tarea(tarea_id)
    
    if not tarea:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontró la tarea con ID {tarea_id}"
        )
    
    return tarea_a_response(tarea)

# Ruta para actualizar una tarea
@app.put("/tareas/{tarea_id}", response_model=TareaResponse)
async def actualizar_tarea(tarea_id: int, tarea_data: TareaUpdate):
    update_data = tarea_data.model_dump(exclude_none=True)
    
    if "estado" in update_data:
        update_data["estado"] = update_data["estado"].value
    if "prioridad" in update_data:
        update_data["prioridad"] = update_data["prioridad"].value
    
    try:
        tarea = gestor.actualizar_tarea(tarea_id, **update_data)
        
        if not tarea:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró la tarea con ID {tarea_id}"
            )
        
        return tarea_a_response(tarea)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar la tarea")

# Ruta para eliminar una tarea
@app.delete("/tareas/{tarea_id}", response_model=MensajeResponse)
async def eliminar_tarea(tarea_id: int):
    if gestor.eliminar_tarea(tarea_id):
        return MensajeResponse(mensaje=f"Tarea {tarea_id} eliminada exitosamente")
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la tarea con ID {tarea_id}"
        )

# Ruta para marcar una tarea como completada
@app.patch("/tareas/{tarea_id}/completar", response_model=TareaResponse)
async def marcar_completada(tarea_id: int):
    tarea = gestor.marcar_completada(tarea_id)
    
    if not tarea:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la tarea con ID {tarea_id}"
        )
    
    return tarea_a_response(tarea)

# Ruta para obtener estadísticas
@app.get("/estadisticas", response_model=EstadisticasResponse)
async def obtener_estadisticas():
    try:
        stats = gestor.obtener_estadisticas()
        return EstadisticasResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener estadísticas")

# Ruta para listar tareas vencidas
@app.get("/tareas/vencidas/listar", response_model=ListaTareasResponse)
async def listar_tareas_vencidas():
    try:
        tareas_vencidas = gestor.obtener_tareas_vencidas()
        tareas_response = [tarea_a_response(t) for t in tareas_vencidas]
        
        return ListaTareasResponse(
            tareas=tareas_response,
            total=len(tareas_response)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener tareas vencidas")

# Manejo de errores globales
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(status_code=400, detail=str(exc))

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Recurso no encontrado"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)