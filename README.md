# Project Backend

Este es el backend de un proyecto que utiliza FastAPI para manejar tareas y listas de tareas. Este proyecto incluye operaciones CRUD completas para tareas y listas de tareas.

## Requisitos

- Python 3.9 o superior
- MongoDB
- Docker (opcional)

## Instalación

1. Clona el repositorio:

   ```sh
   git clone https://github.com/TuUsuario/TuRepositorio.git
   cd TuRepositorio
Crea y activa un entorno virtual:

## Entorno Virtual
python3 -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`
Instala las dependencias:


pip install -r requirements.txt
Configura las variables de entorno. Crea un archivo .env en la raíz del proyecto y define las siguientes variables:


DATABASE_URL=mongodb://localhost:27017


uvicorn app.main:app --reload
La API estará disponible en http://127.0.0.1:8000.

## Endpoints

## Usuarios
POST /users/ - Crear un nuevo usuario
GET /users/ - Obtener todos los usuarios
POST /token - Obtener un token de acceso
Listas de Tareas
POST /task_lists/ - Crear una nueva lista de tareas
GET /task_lists/ - Obtener todas las listas de tareas
GET /task_lists/{task_list_id} - Obtener una lista de tareas por ID
PUT /task_lists/{task_list_id} - Actualizar una lista de tareas
DELETE /task_lists/{task_list_id} - Eliminar una lista de tareas

## Tareas
POST /tasks/ - Crear una nueva tarea
GET /tasks/ - Obtener todas las tareas
GET /tasks/{task_id} - Obtener una tarea por ID
PUT /tasks/{task_id} - Actualizar una tarea
DELETE /tasks/{task_id} - Eliminar una tarea

## Docker
Puedes usar Docker para ejecutar la aplicación en un contenedor.

Construye la imagen de Docker:

docker build -t project-backend .

Ejecuta el contenedor:

docker-compose up
La aplicación estará disponible en http://127.0.0.1:8000.

## Contribuciones
¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.