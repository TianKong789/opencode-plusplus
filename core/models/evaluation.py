from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from core.ids import EvaluationId, ExecutionId


@unique
class Verdict(Enum):
    PASS = "pass"
    PARTIAL = "partial"
    FAIL = "fail"


@dataclass(slots=True, frozen=True)
class Evaluation:
    id: EvaluationId
    execution_id: ExecutionId
    score: float
    verdict: Verdict
    criteria: tuple[str, ...]
    summary: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Evaluation id must not be empty")
        if not self.execution_id:
            raise ValueError("Evaluation execution_id must not be empty")
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Evaluation score must be between 0.0 and 1.0")

    def is_passing(self) -> bool:
        return self.verdict == Verdict.PASS
