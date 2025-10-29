from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.task import Task

class TaskRepository(ABC):
    """
    Puerto (interfaz) para persistir y recuperar tareas.

    Este puerto permite aplicar DIP: la capa de aplicación depende de la
    abstracción, no de una implementación concreta.
    """

    @abstractmethod
    def list_tasks(self) -> List[Task]: ...
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]: ...
    @abstractmethod
    def add(self, task: Task) -> Task: ...
    @abstractmethod
    def update(self, task: Task) -> Task: ...
    @abstractmethod
    def delete(self, task_id: int) -> None: ...
