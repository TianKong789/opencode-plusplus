from __future__ import annotations

from dataclasses import dataclass

from core.ids import TaskId, WorkspaceId


@dataclass(slots=True, frozen=True)
class Workspace:
    id: WorkspaceId
    name: str
    root_path: str
    task_ids: tuple[TaskId, ...] = ()
    active: bool = True

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Workspace id must not be empty")
        if not self.name:
            raise ValueError("Workspace name must not be empty")
        if not self.root_path:
            raise ValueError("Workspace root_path must not be empty")

    def task_count(self) -> int:
        return len(self.task_ids)
