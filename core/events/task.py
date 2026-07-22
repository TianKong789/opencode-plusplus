from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class TaskCreated(BaseEvent):
    """Emitted when a new task enters the system."""

    task_id: str = ""
    title: str = ""


@dataclass(slots=True, frozen=True)
class TaskReceived(BaseEvent):
    """Emitted when the application orchestrator receives a task."""

    task_id: str = ""
    title: str = ""
