from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class PlanGenerated(BaseEvent):
    """Emitted when the Planner produces a new plan for a task."""

    plan_id: str = ""
    task_id: str = ""
    step_count: int = 0
