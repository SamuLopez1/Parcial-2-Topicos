from __future__ import annotations
from typing import Optional
from app.ports.task_repository import TaskRepository
from app.domain.task import Task, TaskStatus

class TaskService:
    """
    Servicio de aplicación que coordina casos de uso de tareas.

    Aplica SRP (una única responsabilidad: orquestar casos de uso), DIP (depende
    de un `TaskRepository` abstracto) y facilita OCP (nuevas operaciones sin
    tocar el dominio).
    """

    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def list_tasks(self) -> list[Task]:
        """Retorna todas las tareas."""
        return self._repo.list_tasks()

    def create_task(self, title: str, status: TaskStatus) -> Task:
        """Crea una tarea válida y la persiste."""
        task = Task.create(title, status)
        return self._repo.add(task)

    def get_task(self, task_id: int) -> Task:
        """Obtiene una tarea o lanza ValueError si no existe."""
        t = self._repo.get_by_id(task_id)
        if not t:
            raise ValueError("Tarea no encontrada")
        return t

    def update_task(self, task_id: int, title: Optional[str] = None, status: Optional[TaskStatus] = None) -> Task:
        """Actualiza título y/o estado de una tarea existente."""
        current = self.get_task(task_id)
        new_title = current.title if title is None else title.strip()
        if new_title == "":
            raise ValueError("El título no puede estar vacío.")
        new_status = current.status if status is None else status
        updated = Task(id=current.id, title=new_title, status=new_status)
        return self._repo.update(updated)

    def delete_task(self, task_id: int) -> None:
        """Elimina una tarea (idempotente)."""
        self._repo.delete(task_id)
