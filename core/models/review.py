from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from core.ids import ArtifactId, ReviewId


@unique
class ReviewVerdict(Enum):
    APPROVE = "approve"
    REQUEST_CHANGES = "request_changes"
    COMMENT = "comment"


@dataclass(slots=True, frozen=True)
class Review:
    """A code review of a CodeArtifact."""

    id: ReviewId
    artifact_id: ArtifactId
    score: float
    verdict: ReviewVerdict
    findings: tuple[str, ...] = ()
    suggestions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Review id must not be empty")
        if not self.artifact_id:
            raise ValueError("Review artifact_id must not be empty")
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Review score must be between 0.0 and 1.0")

    def is_approved(self) -> bool:
        return self.verdict == ReviewVerdict.APPROVE
