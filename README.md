# Tasks API — FastAPI · SOLID · Docker

API REST sencilla para gestión de tareas (Python 3.11 + FastAPI). Diseñada con separación por capas (Domain / Application / Adapters) y principios SOLID. Se puede ejecutar localmente o en Docker (puerto 8000 por defecto).

---

## Tabla de contenidos
- [Descripción](#descripción)
- [Características](#características)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y ejecución (local)](#instalación-y-ejecución-local)
- [Ejecución con Docker](#ejecución-con-docker)
- [Endpoints](#endpoints)
- [Ejemplos con curl](#ejemplos-con-curl)
- [Pruebas](#pruebas)
- [Diagnóstico rápido si el README no se ve](#diagnóstico-rápido-si-el-readme-no-se-ve)
- [Decisiones técnicas y limitaciones](#decisiones-técnicas-y-limitaciones)

## Descripción
API para crear, listar, actualizar y eliminar tareas en memoria. Pensada para ser fácil de leer y extender (por ejemplo, cambiar el repositorio en memoria por SQLite sin tocar la capa de aplicación).

## Características
- GET /tasks: listar tareas
- POST /tasks: crear tarea (title, status ∈ {pending, done})
- GET /tasks/{id}: obtener tarea por id
- PUT /tasks/{id}: actualizar tarea
- DELETE /tasks/{id}: eliminar tarea (idempotente)
- GET /health: estado del servicio
- Validaciones: title obligatorio, status solo "pending" o "done"

## Estructura del proyecto
app/
  domain/
  application/
  ports/
  adapters/
requirements.txt  
Dockerfile  
README.md

(Ver README interno para detalle por carpeta)

## Requisitos
- Python 3.10+ (probado en 3.11)
- pip actualizado
- Docker (opcional)

## Instalación y ejecución (local)
Crear entorno virtual e instalar dependencias:

Windows:
```powershell
python -m venv venv
venv\Scripts\Activate.ps1   # o venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.adapters.http.fastapi_app:app --reload
```

Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.adapters.http.fastapi_app:app --reload
```

Swagger/OpenAPI: http://127.0.0.1:8000/docs  
Health: http://127.0.0.1:8000/health

## Ejecución con Docker
Construir y ejecutar:
```bash
docker build -t tasks-api .
docker run -d --name tasks -p 8000:8000 tasks-api
```
Comando único:
```bash
docker build -t tasks-api . && docker run -d --name tasks -p 8000:8000 tasks-api
```
Ver logs:
```bash
docker logs -f tasks
```

## Endpoints
- GET /health → { "status": "ok" }
- GET /tasks → lista de tareas
- POST /tasks → crear tarea: { "title": "Estudiar Docker", "status": "pending" }
- GET /tasks/{id} → obtener por id
- PUT /tasks/{id} → actualizar: { "title":"nuevo","status":"done" }
- DELETE /tasks/{id} → eliminar (idempotente)

## Ejemplos con curl (Windows CMD / PowerShell adaptando comillas)
Crear:
```bash
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Examen\",\"status\":\"pending\"}"
```
Listar:
```bash
curl http://127.0.0.1:8000/tasks
```
Obtener:
```bash
curl http://127.0.0.1:8000/tasks/1
```
Actualizar:
```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d "{\"title\":\"Examen final\",\"status\":\"done\"}"
```
Eliminar:
```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Pruebas
Si existen tests (pytest):
```bash
pip install pytest
python -m pytest -q
```

## Diagnóstico rápido si el README no se ve en GitHub
1. Nombre: el archivo debe llamarse exactamente `README.md` y estar en la raíz de la rama por defecto.
2. Comprobar estado git:
```bash
git ls-files | grep -i readme
git status
git branch -v
```
3. Codificación: debe estar en UTF-8 sin BOM. Para comprobar:
```bash
file -bi README.md
```
Si aparece bom, re-guardar como "UTF-8 sin BOM" desde el editor.

## Decisiones técnicas y limitaciones
- Persistencia en memoria (los datos se pierden al reiniciar).
- Diseño por capas (Repository + Service) para facilitar cambios de infra.
- Pydantic v2 para DTOs y validaciones en adaptador HTTP.

---

Si quieres, puedo ajustar el texto (idioma, más detalle técnico o badges) o generar un README traducido a inglés.