from __future__ import annotations

from dataclasses import dataclass

from core.ids import ResearchId, TaskId


@dataclass(slots=True, frozen=True)
class Research:
    """Research findings gathered for a task."""

    id: ResearchId
    task_id: TaskId
    findings: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    summary: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Research id must not be empty")
        if not self.task_id:
            raise ValueError("Research task_id must not be empty")

    def has_findings(self) -> bool:
        return len(self.findings) > 0
