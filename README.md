Una API REST sencilla para gestionar tareas, aplicando los 4 pilares de la Programación Orientada a Objetos.

##🎯 Características

✅ CRUD completo de tareas (Crear, Leer, Actualizar, Eliminar)
✅ 3 tipos de tareas: Simple, Prioritaria, Con fecha límite
✅ Estados de tareas: Pendiente, En progreso, Completada
✅ Estadísticas y filtros
✅ Documentación automática con Swagger UI

##🏗️ Pilares de POO Implementados

1. Encapsulación 🔒
Atributos privados en las clases (_id, _titulo, etc.)
Getters y setters para controlar el acceso
Validación de datos en los setters

2. Abstracción 🎭
Clase abstracta TareaBase con método obtener_info_especifica()
Interface simple del GestorTareas que oculta la complejidad interna
Separación clara entre lógica de negocio y endpoints

3. Herencia 🌳
TareaSimple, TareaPrioritaria y TareaConFecha heredan de TareaBase
Reutilización de código común
Especialización de comportamientos

4. Polimorfismo 🎪
Método obtener_info_especifica() implementado diferente en cada subclase
marcar_completada() sobrescrito en TareaPrioritaria
El gestor maneja todos los tipos de tareas uniformemente

##⚙️ Stack Tecnológico:

Backend:
- Python 3.8+
- FastAPI (API REST)
- Pydantic (validación datos)
- Uvicorn (servidor ASGI)

Frontend:
- HTML5 + CSS3
- JavaScript ES6+
- Diseño responsivo

Persistencia:
- JSON (archivos locales)

##🚀 Instalación y Uso
1. Instalar dependencias
pip install fastapi uvicorn pydantic
pip install Jinga2
2. Ejecutar el servidor
uvicorn main:app --reload

##📊 Endpoints Principales

Tareas
POST /tareas - Crear nueva tarea
GET /tareas - Listar todas las tareas
GET /tareas/{id} - Obtener tarea específica
PUT /tareas/{id} - Actualizar tarea
DELETE /tareas/{id} - Eliminar tarea
PATCH /tareas/{id}/completar - Marcar tarea como completada
Estadísticas y Filtros
GET /estadisticas - Obtener estadísticas de tareas
GET /tareas/vencidas/listar - Listar tareas vencidas
