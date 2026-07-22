from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class WorkflowStarted(BaseEvent):
    """Emitted when the WorkflowRunner begins executing a workflow."""

    workflow_id: str = ""
    step_count: int = 0


@dataclass(slots=True, frozen=True)
class StepStarted(BaseEvent):
    """Emitted when the WorkflowRunner begins executing a single step."""

    workflow_id: str = ""
    step_id: str = ""
    step_name: str = ""


@dataclass(slots=True, frozen=True)
class StepCompleted(BaseEvent):
    """Emitted when the WorkflowRunner finishes executing a single step."""

    workflow_id: str = ""
    step_id: str = ""
    step_name: str = ""
    success: bool = False
    duration_ms: float = 0.0


@dataclass(slots=True, frozen=True)
class WorkflowCompleted(BaseEvent):
    """Emitted when the WorkflowRunner finishes executing a workflow."""

    workflow_id: str = ""
    success: bool = False
    step_count: int = 0
