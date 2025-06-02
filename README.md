# FastAPI---Gestion-de-Tareas

📘 ¿Qué es FastAPI?
FastAPI es un framework moderno y rápido para construir APIs web utilizando el lenguaje de programación Python.
API (Interfaz de Programación de Aplicaciones): Es un conjunto de reglas que permiten que diferentes aplicaciones se comuniquen entre sí.


Framework: Es una herramienta que proporciona una estructura base para desarrollar software de forma más rápida y organizada.


FastAPI permite crear aplicaciones web que pueden recibir datos, procesarlos y responder a solicitudes. Es muy usado para desarrollar el "backend" de aplicaciones modernas.

🚀 ¿Por qué usamos FastAPI en este proyecto?
Simplicidad y velocidad: Nos permite crear rápidamente un sistema web funcional.


Documentación automática: Al escribir el código, FastAPI genera una interfaz web donde podemos probar la API sin escribir documentación extra.


Compatibilidad con Python moderno: Utiliza tipos de datos y anotaciones, lo que mejora la claridad del código.


Buen rendimiento: Es una de las opciones más rápidas disponibles en Python.



🧠 ¿Qué haremos con FastAPI en este proyecto?
🎯 Objetivo:
Construir una API para gestionar tareas. Las tareas son pequeños trabajos o recordatorios que el usuario puede:
Crear


Consultar


Actualizar


Eliminar


Este tipo de operación se conoce como CRUD (Create, Read, Update, Delete).

🛠️ ¿Cómo se organiza el proyecto?
La aplicación se divide en partes claras para aplicar Programación Orientada a Objetos (POO):
Archivo
Contenido
main.py
Punto de entrada. Define los endpoints (URLs de la API).
models.py
Clases que representan las tareas (y variantes).
gestor.py
Clase que maneja la lógica para almacenar y modificar tareas.
schemas.py
Estructuras de datos usadas para validar entradas y salidas.
README.md
Documentación explicando qué hace el proyecto y cómo usarlo.


🔍 ¿Qué se aprende con este proyecto?
Cómo crear una API REST con FastAPI.


Cómo usar clases en Python para organizar datos y lógica (POO).


Cómo aplicar los cuatro pilares de la programación orientada a objetos:


Encapsulación: ocultar los detalles internos.


Abstracción: separar el "qué hace" del "cómo lo hace".


Herencia: crear clases nuevas a partir de otras.


Polimorfismo: permitir que clases relacionadas se comporten de forma diferente.


Cómo enviar y recibir información en formato JSON (el más común en APIs).


Cómo separar el código en partes reutilizables y fáciles de entender.

------

API Gestor de Tareas - FastAPI + POO
Una API REST sencilla para gestionar tareas, aplicando los 4 pilares de la Programación Orientada a Objetos.
🎯 Características

✅ CRUD completo de tareas (Crear, Leer, Actualizar, Eliminar)
✅ 3 tipos de tareas: Simple, Prioritaria, Con fecha límite
✅ Estados de tareas: Pendiente, En progreso, Completada
✅ Estadísticas y filtros
✅ Documentación automática con Swagger UI

🏗️ Pilares de POO Implementados
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

📁 Estructura del Proyecto
todo_api/
│
├── main.py                 # App FastAPI + endpoints
├── models.py              # Clases POO (TareaBase y variantes)
├── gestor.py              # Clase GestorTareas (lógica)
├── schemas.py             # Modelos Pydantic (validación)
└── README.md              # Documentación
🚀 Instalación y Uso
1. Instalar dependencias
bashpip install fastapi uvicorn pydantic
2. Ejecutar el servidor
bashpython main.py
3. Acceder a la documentación

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

📊 Endpoints Principales
Tareas

POST /tareas - Crear nueva tarea
GET /tareas - Listar todas las tareas
GET /tareas/{id} - Obtener tarea específica
PUT /tareas/{id} - Actualizar tarea
