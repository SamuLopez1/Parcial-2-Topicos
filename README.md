Tasks API — FastAPI · SOLID · Docker

API REST de gestión de tareas en Python 3.11 con FastAPI, diseñada con separación por capas y principios SOLID. Se ejecuta localmente o en Docker (puerto 8000).

Objetivo y Alcance

API REST sencilla que expone:

GET /tasks: lista tareas.

POST /tasks: crea tarea con title y status ∈ {pending, done}.

GET /health: verifica estado del servicio.

Extensiones incluidas:

GET /tasks/{id}: obtiene una tarea por ID.

PUT /tasks/{id}: actualiza título y/o estado.

DELETE /tasks/{id}: elimina una tarea (idempotente).

Persistencia en memoria (diccionario). Puede reemplazarse por SQLite sin tocar la capa de aplicación.

Validaciones mínimas

title obligatorio y no vacío.

status debe ser "pending" o "done".

Datos inválidos → 400 Bad Request.

Recurso inexistente → 404 Not Found.

Arquitectura y Diseño

Capas:

Dominio (app/domain): entidad Task, enum TaskStatus, reglas de negocio y factory.

Aplicación (app/application): TaskService (casos de uso).

Adaptadores (app/adapters):

HTTP (FastAPI): controladores y DTOs/Pydantic.

Persistencia: implementación en memoria del repositorio.

Patrones aplicados:

Repository: aísla la persistencia (puerto TaskRepository).

Service / Use Case: orquestación de casos de uso (TaskService).

Factory: Task.create(...) garantiza entidades válidas.

Principios SOLID:

SRP: dominio, servicio y adaptadores con responsabilidades claras.

OCP: agregar nuevas operaciones o persistencias sin modificar el dominio.

DIP: la aplicación depende de la interfaz TaskRepository, no de la implementación.

Estructura de carpetas
app/
  domain/
    task.py
  application/
    services/
      task_service.py
  ports/
    task_repository.py
  adapters/
    http/
      fastapi_app.py
    persistence/
      memory_task_repository.py
requirements.txt
Dockerfile
README.md

Requisitos

Python 3.10 o superior (probado con 3.11).

Pip actualizado.

Docker Desktop (opcional para ejecución en contenedor).

Instalación y ejecución (local)
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python -m uvicorn app.adapters.http.fastapi_app:app --reload


Swagger/OpenAPI: http://127.0.0.1:8000/docs

Health: http://127.0.0.1:8000/health

Ejecución con Docker
docker build -t tasks-api .
docker run -d --name tasks -p 8000:8000 tasks-api


Comando único (build + run en una línea):

docker build -t tasks-api . && docker run -d --name tasks -p 8000:8000 tasks-api


Ver logs:

docker logs -f tasks


Nota: si el puerto 8000 está ocupado, usa -p 8001:8000 y prueba http://127.0.0.1:8001/health

Endpoints

GET /health
Respuesta: {"status": "ok"}

GET /tasks
Lista todas las tareas.

POST /tasks
Cuerpo JSON:

{ "title": "Estudiar Docker", "status": "pending" }


GET /tasks/{id}
Obtiene una tarea por su ID.

PUT /tasks/{id}
Cuerpo JSON:

{ "title": "Estudiar Docker y FastAPI", "status": "done" }


DELETE /tasks/{id}
Elimina la tarea.

Ejemplos con curl (CMD, una línea por comando)
:: Health
curl http://127.0.0.1:8000/health

:: Listar (vacío al inicio)
curl http://127.0.0.1:8000/tasks

:: Crear
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Examen\",\"status\":\"pending\"}"

:: Obtener por ID
curl http://127.0.0.1:8000/tasks/1

:: Actualizar
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d "{\"title\":\"Examen final\",\"status\":\"done\"}"

:: Eliminar
curl -X DELETE http://127.0.0.1:8000/tasks/1

Pruebas (opcional)

Requisitos: pytest

Ejecución:

pip install pytest
python -m pytest -q

Decisiones técnicas

Persistencia en memoria para cumplir el alcance mínimo y mantener bajo el tiempo de implementación.

Separación por capas con Repository + Service para facilitar reemplazo de infraestructura (por ejemplo, SQLite) sin afectar la lógica de aplicación.

DTOs de entrada/salida con Pydantic v2 para validaciones en el adaptador HTTP.

Limitaciones

Almacén en memoria: los datos se pierden al reiniciar el proceso o el contenedor.