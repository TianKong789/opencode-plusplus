from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from core.ids import ArtifactId, PlanId


@unique
class ArtifactStatus(Enum):
    GENERATED = "generated"
    REVIEWED = "reviewed"
    TESTED = "tested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(slots=True, frozen=True)
class CodeArtifact:
    """A code artifact produced by implementing a plan."""

    id: ArtifactId
    plan_id: PlanId
    files: tuple[str, ...]
    language: str = "python"
    summary: str = ""
    status: ArtifactStatus = ArtifactStatus.GENERATED

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Artifact id must not be empty")
        if not self.plan_id:
            raise ValueError("Artifact plan_id must not be empty")

    def is_accepted(self) -> bool:
        return self.status == ArtifactStatus.ACCEPTED
