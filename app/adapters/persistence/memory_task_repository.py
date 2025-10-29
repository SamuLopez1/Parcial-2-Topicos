from __future__ import annotations
from typing import List, Optional, Dict
from threading import Lock
from app.ports.task_repository import TaskRepository
from app.domain.task import Task

class MemoryTaskRepository(TaskRepository):
    """Repositorio en memoria (thread-safe básico con Lock)."""

    def __init__(self) -> None:
        self._items: Dict[int, Task] = {}
        self._seq = 1
        self._lock = Lock()

    def list_tasks(self) -> List[Task]:
        return list(self._items.values())

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._items.get(task_id)

    def add(self, task: Task) -> Task:
        with self._lock:
            tid = self._seq
            self._seq += 1
        saved = Task(id=tid, title=task.title, status=task.status)
        self._items[tid] = saved
        return saved

    def update(self, task: Task) -> Task:
        if task.id is None or task.id not in self._items:
            raise KeyError("No existe la tarea con ese ID")
        self._items[task.id] = task
        return task

    def delete(self, task_id: int) -> None:
        self._items.pop(task_id, None)
    