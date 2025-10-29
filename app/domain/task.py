from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    """Estados válidos de una tarea."""
    pending = "pending"
    done = "done"

@dataclass(frozen=True)
class Task:
    """
    Entidad de dominio que representa una tarea.

    Attributes:
        id: Identificador único (lo asigna el repositorio).
        title: Título descriptivo de la tarea.
        status: Estado de la tarea (pending/done).
    """
    id: Optional[int]
    title: str
    status: TaskStatus

    @staticmethod
    def create(title: str, status: TaskStatus) -> "Task":
        """
        Factory para construir una tarea válida sin ID.

        Args:
            title: Título de la tarea; no puede estar vacío.
            status: Estado inicial (pending/done).

        Raises:
            ValueError: Si `title` está vacío.

        Returns:
            Task: nueva entidad sin id (id=None).
        """
        if not title or not title.strip():
            raise ValueError("El título no puede estar vacío.")
        return Task(id=None, title=title.strip(), status=status)
