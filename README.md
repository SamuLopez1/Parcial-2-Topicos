# Tasks API — FastAPI · SOLID · Docker

API REST mínima de gestión de tareas (to-do) implementada en Python 3.11 con FastAPI. Aplica separación por capas (dominio, aplicación, adaptadores), principios SOLID y se ejecuta con Docker.

## Endpoints
- `GET /health`
- `GET /tasks`
- `POST /tasks`  (body: `{"title":"...", "status":"pending|done"}`)
- `GET /tasks/{id}`
- `PUT /tasks/{id}`
- `DELETE /tasks/{id}`

## Ejecutar local       
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

uvicorn app.adapters.http.fastapi_app:app --reload
# http://127.0.0.1:8000/docs