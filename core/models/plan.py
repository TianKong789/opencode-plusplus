from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from core.ids import PlanId, TaskId


@unique
class PlanStatus(Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


@dataclass(slots=True, frozen=True)
class Plan:
    id: PlanId
    task_id: TaskId
    strategy: str
    steps: tuple[str, ...]
    status: PlanStatus = PlanStatus.DRAFT

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Plan id must not be empty")
        if not self.task_id:
            raise ValueError("Plan task_id must not be empty")
        if not self.steps:
            raise ValueError("Plan must have at least one step")

    def step_count(self) -> int:
        return len(self.steps)
