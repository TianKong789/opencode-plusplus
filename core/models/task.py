from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique


@unique
class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True, frozen=True)
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Task id must not be empty")
        if not self.title:
            raise ValueError("Task title must not be empty")

    def is_terminal(self) -> bool:
        return self.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED)
