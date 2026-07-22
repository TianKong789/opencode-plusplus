from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from core.ids import ArtifactId, TestResultId


@unique
class TestVerdict(Enum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"


@dataclass(slots=True, frozen=True)
class TestResult:
    """Test results for a CodeArtifact."""

    id: TestResultId
    artifact_id: ArtifactId
    verdict: TestVerdict
    passed: int = 0
    failed: int = 0
    errors: tuple[str, ...] = ()
    summary: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("TestResult id must not be empty")
        if not self.artifact_id:
            raise ValueError("TestResult artifact_id must not be empty")
        if self.passed < 0:
            raise ValueError("TestResult passed must not be negative")
        if self.failed < 0:
            raise ValueError("TestResult failed must not be negative")

    def is_passing(self) -> bool:
        return self.verdict == TestVerdict.PASS

    def total(self) -> int:
        return self.passed + self.failed
