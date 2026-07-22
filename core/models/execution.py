from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from core.ids import ExecutionId, PlanId


@unique
class ExecutionStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


@dataclass(slots=True, frozen=True)
class Execution:
    id: ExecutionId
    plan_id: PlanId
    status: ExecutionStatus = ExecutionStatus.QUEUED
    outputs: tuple[str, ...] = ()
    error: str | None = None
    duration_ms: float | None = None

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Execution id must not be empty")
        if not self.plan_id:
            raise ValueError("Execution plan_id must not be empty")
        if self.duration_ms is not None and self.duration_ms < 0:
            raise ValueError("Execution duration_ms must not be negative")

    def is_terminal(self) -> bool:
        return self.status in (
            ExecutionStatus.COMPLETED,
            ExecutionStatus.FAILED,
            ExecutionStatus.TIMED_OUT,
        )

    def succeeded(self) -> bool:
        return self.status == ExecutionStatus.COMPLETED
