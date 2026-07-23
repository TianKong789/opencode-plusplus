from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True, frozen=True)
class TaskDefinition:
    task_id: str
    input_data: str
    expected_output: str
    capability: str
    difficulty: str = "basic"


@dataclass(slots=True, frozen=True)
class TaskResult:
    task_id: str
    output: str
    score: float
    latency_ms: float = 0.0
    tokens_used: int = 0

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Task score must be between 0.0 and 1.0")


@dataclass
class TestSuiteResult:
    capability: str
    results: tuple[TaskResult, ...] = ()
    average_score: float = 0.0
    total_tasks: int = 0
    passed_tasks: int = 0


@dataclass
class TestRunner:
    benchmark_dir: Path = field(default_factory=lambda: Path("benchmarks/capabilities"))

    def load_tasks(self, capability: str) -> tuple[TaskDefinition, ...]:
        metadata_path = self.benchmark_dir / capability / "metadata.json"
        if not metadata_path.exists():
            return ()

        metadata = json.loads(metadata_path.read_text())
        tasks = metadata.get("tasks", ())
        return tuple(
            TaskDefinition(
                task_id=task["task_id"],
                input_data=task["input_data"],
                expected_output=task["expected_output"],
                capability=metadata.get("capability", capability),
                difficulty=task.get("difficulty", "basic"),
            )
            for task in tasks
        )

    def run_suite(
        self,
        capability: str,
        executor: Callable[[str], str],
        tasks: tuple[TaskDefinition, ...] | None = None,
    ) -> TestSuiteResult:
        suite_tasks = self.load_tasks(capability) if tasks is None else tasks
        results = tuple(
            TaskResult(
                task_id=task.task_id,
                output=output,
                score=1.0 if output == task.expected_output else 0.0,
            )
            for task in suite_tasks
            for output in (executor(task.input_data),)
        )
        total_tasks = len(results)
        return TestSuiteResult(
            capability=capability,
            results=results,
            average_score=(sum(result.score for result in results) / total_tasks)
            if total_tasks
            else 0.0,
            total_tasks=total_tasks,
            passed_tasks=sum(result.score >= 0.7 for result in results),
        )
