from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class ExecutionStarted(BaseEvent):
    """Emitted when an Executor begins running a plan."""

    execution_id: str = ""
    plan_id: str = ""


@dataclass(slots=True, frozen=True)
class ExecutionCompleted(BaseEvent):
    """Emitted when an ExecutionEngine finishes running code."""

    execution_id: str = ""
    plan_id: str = ""
    success: bool = False
    duration_ms: float = 0.0
