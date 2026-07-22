"""Test suite runner for capability assessments.

Executes task suites and collects results for scoring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TaskDefinition:
    """Definition of a benchmark task.

    Attributes:
        task_id: Unique identifier for the task.
        input_data: The task input/prompt.
        expected_output: The expected output (for scoring).
        capability: The capability being tested.
        difficulty: Task difficulty level.
    """

    task_id: str
    input_data: str
    expected_output: str
    capability: str
    difficulty: str = "basic"


@dataclass
class TaskResult:
    """Result of executing a single task.

    Attributes:
        task_id: The task that was executed.
        output: The actual output produced.
        score: The score (0.0 to 1.0).
        latency_ms: Execution latency in milliseconds.
        tokens_used: Number of tokens consumed.
    """

    task_id: str
    output: str
    score: float
    latency_ms: float = 0.0
    tokens_used: int = 0

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"score must be 0.0-1.0, got {self.score}")


@dataclass
class TestSuiteResult:
    """Aggregated results from a test suite execution.

    Attributes:
        capability: The capability that was tested.
        results: Individual task results.
        average_score: Mean score across all tasks.
        total_tasks: Total number of tasks.
        passed_tasks: Number of tasks with score >= 0.7.
    """

    capability: str
    results: tuple[TaskResult, ...] = ()
    average_score: float = 0.0
    total_tasks: int = 0
    passed_tasks: int = 0


@dataclass
class TestRunner:
    """Runs capability test suites.

    Loads tasks from benchmark directories and executes them
    against a model.
    """

    benchmark_dir: Path = field(default_factory=lambda: Path("benchmarks/capabilities"))

    def load_tasks(self, capability: str) -> tuple[TaskDefinition, ...]:
        """Load tasks for a specific capability.

        Args:
            capability: The capability to load tasks for.

        Returns:
            A tuple of task definitions.
        """
        tasks_dir = self.benchmark_dir / capability / "tasks"
        if not tasks_dir.exists():
            return ()

        # Placeholder - would load from JSON/YAML files
        return ()

    def run_suite(
        self,
        capability: str,
        executor: callable,
    ) -> TestSuiteResult:
        """Run a complete test suite for a capability.

        Args:
            capability: The capability to test.
            executor: A callable that takes task input and returns output.

        Returns:
            Aggregated test suite results.
        """
        tasks = self.load_tasks(capability)
        results = []

        for task in tasks:
            # Execute task
            output = executor(task.input_data)

            # Score output (placeholder - would use Scorer)
            score = 1.0 if output == task.expected_output else 0.0

            results.append(TaskResult(
                task_id=task.task_id,
                output=output,
                score=score,
            ))

        # Calculate aggregates
        total = len(results)
        passed = sum(1 for r in results if r.score >= 0.7)
        avg_score = sum(r.score for r in results) / total if total > 0 else 0.0

        return TestSuiteResult(
            capability=capability,
            results=tuple(results),
            average_score=avg_score,
            total_tasks=total,
            passed_tasks=passed,
        )
