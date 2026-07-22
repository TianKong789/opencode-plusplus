from __future__ import annotations

from dataclasses import dataclass

from core.ids import BenchmarkId, SkillId


@dataclass(slots=True, frozen=True)
class Benchmark:
    id: BenchmarkId
    skill_id: SkillId
    name: str
    input_data: str
    expected_output: str
    timeout_ms: float = 30000.0

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Benchmark id must not be empty")
        if not self.skill_id:
            raise ValueError("Benchmark skill_id must not be empty")
        if not self.name:
            raise ValueError("Benchmark name must not be empty")
        if self.timeout_ms <= 0:
            raise ValueError("Benchmark timeout_ms must be positive")
