from __future__ import annotations
from typing import List, Optional, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from app.adapters.persistence.memory_task_repository import MemoryTaskRepository
from app.application.services.task_service import TaskService
from app.domain.task import Task, TaskStatus

app = FastAPI(
    title="Tasks API",
    version="1.0.0",
    description="API de gestión de tareas (FastAPI + SOLID + Docker)"
)

# Wiring simple (DIP por constructor ya aplicado en el servicio)
_repo = MemoryTaskRepository()
_service = TaskService(_repo)

class TaskIn(BaseModel):
    title: str
    status: Literal["pending", "done"] = "pending"

    @field_validator("title")
    @classmethod
    def _check_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("title no puede estar vacío")
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[Literal["pending", "done"]] = None

    @field_validator("title")
    @classmethod
    def _check_title(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("title no puede estar vacío")
        return v.strip()

class TaskOut(BaseModel):
    id: int
    title: str
    status: Literal["pending", "done"]

    @staticmethod
    def from_domain(task: Task) -> "TaskOut":
        return TaskOut(id=task.id, title=task.title, status=task.status.value)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/tasks", response_model=List[TaskOut])
def list_tasks() -> List[TaskOut]:
    tasks = _service.list_tasks()
    return [TaskOut.from_domain(t) for t in tasks]

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskIn) -> TaskOut:
    try:
        t = _service.create_task(payload.title, TaskStatus(payload.status))
        return TaskOut.from_domain(t)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Extras (recomendados en el enunciado):
@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int) -> TaskOut:
    try:
        t = _service.get_task(task_id)
        return TaskOut.from_domain(t)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate) -> TaskOut:
    try:
        new_status = TaskStatus(payload.status) if payload.status is not None else None
        t = _service.update_task(task_id, title=payload.title, status=new_status)
        return TaskOut.from_domain(t)
    except ValueError as e:
        if "no encontrada" in str(e).lower() or "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Task not found")
    raise HTTPException(status_code=400, detail=str(e))

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    _service.delete_task(task_id)
    return None
