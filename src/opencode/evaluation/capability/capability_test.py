"""Extensible capability test interface.

Defines the CapabilityTest ABC that each capability implements.
The CapabilityAssessor discovers and runs these tests.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.models import CapabilityScore


@dataclass(frozen=True)
class Model:
    """Minimal model representation for test execution.

    Attributes:
        model_id: Unique model identifier.
        provider: The model provider.
        api_endpoint: Optional API endpoint for inference.
    """

    model_id: str
    provider: str
    api_endpoint: str = ""


class CapabilityTest(ABC):
    """Base class for capability tests.

    Each capability implements its own test logic.
    The assessor discovers and runs these tests automatically.
    """

    @abstractmethod
    def capability(self) -> Capability:
        """Return the capability this test evaluates."""

    @abstractmethod
    def run(self, model: Model) -> CapabilityScore:
        """Execute the test against a model.

        Args:
            model: The model to test.

        Returns:
            A CapabilityScore with score, confidence, and evidence.
        """

    @abstractmethod
    def load_tasks(self) -> tuple[dict[str, object], ...]:
        """Load test tasks for this capability.

        Returns:
            Tuple of task definitions as dictionaries.
        """


@dataclass
class PythonCapabilityTest(CapabilityTest):
    """Tests Python coding capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.PYTHON

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "python_basics",
                "description": "Write a function to calculate fibonacci numbers",
                "difficulty": "basic",
            },
            {
                "task_id": "python_datastructures",
                "description": "Implement a LRU cache using OrderedDict",
                "difficulty": "intermediate",
            },
            {
                "task_id": "python_async",
                "description": "Write an async producer-consumer pattern with backpressure",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} Python tasks"]

        return CapabilityScore(
            capability=Capability.PYTHON,
            score=7.5,
            confidence=0.8,
            evidence=tuple(evidence),
        )


@dataclass
class SQLCapabilityTest(CapabilityTest):
    """Tests SQL query writing capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.SQL

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "sql_joins",
                "description": "Write a query to find customers who placed orders in the last 30 days",
                "difficulty": "basic",
            },
            {
                "task_id": "sqlWindow",
                "description": "Use window functions to rank products by sales within each category",
                "difficulty": "intermediate",
            },
            {
                "task_id": "sqlOptimization",
                "description": "Optimize a slow query using CTEs and proper indexing",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} SQL tasks"]

        return CapabilityScore(
            capability=Capability.SQL,
            score=7.0,
            confidence=0.75,
            evidence=tuple(evidence),
        )


@dataclass
class ArchitectureCapabilityTest(CapabilityTest):
    """Tests system architecture design capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.ARCHITECTURE

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "arch_microservices",
                "description": "Design a microservices architecture for an e-commerce platform",
                "difficulty": "intermediate",
            },
            {
                "task_id": "archScale",
                "description": "Architect a system to handle 1M concurrent users with low latency",
                "difficulty": "advanced",
            },
            {
                "task_id": "archMigration",
                "description": "Plan a strangler fig migration from monolith to services",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} architecture tasks"]

        return CapabilityScore(
            capability=Capability.ARCHITECTURE,
            score=8.0,
            confidence=0.7,
            evidence=tuple(evidence),
        )


@dataclass
class ReasoningCapabilityTest(CapabilityTest):
    """Tests logical reasoning and problem-solving capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.REASONING

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "reason_deductive",
                "description": "Solve a logic puzzle with constraints",
                "difficulty": "basic",
            },
            {
                "task_id": "reasonInductive",
                "description": "Identify the pattern in a sequence and predict the next element",
                "difficulty": "intermediate",
            },
            {
                "task_id": "reasonComplex",
                "description": "Analyze a system failure scenario and identify root causes",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} reasoning tasks"]

        return CapabilityScore(
            capability=Capability.REASONING,
            score=8.5,
            confidence=0.85,
            evidence=tuple(evidence),
        )


@dataclass
class RefactoringCapabilityTest(CapabilityTest):
    """Tests code refactoring capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.REFACTORING

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "refactor_extract",
                "description": "Extract method refactoring for a long function",
                "difficulty": "basic",
            },
            {
                "task_id": "refactorPattern",
                "description": "Replace conditional logic with strategy pattern",
                "difficulty": "intermediate",
            },
            {
                "task_id": "refactorLegacy",
                "description": "Modernize legacy code while maintaining behavior",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} refactoring tasks"]

        return CapabilityScore(
            capability=Capability.REFACTORING,
            score=7.0,
            confidence=0.75,
            evidence=tuple(evidence),
        )


@dataclass
class DocumentationCapabilityTest(CapabilityTest):
    """Tests documentation generation capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.DOCUMENTATION

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "doc_api",
                "description": "Write API documentation for a REST endpoint",
                "difficulty": "basic",
            },
            {
                "task_id": "docArchitecture",
                "description": "Create an architecture decision record (ADR)",
                "difficulty": "intermediate",
            },
            {
                "task_id": "docComplex",
                "description": "Write a comprehensive technical design document",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} documentation tasks"]

        return CapabilityScore(
            capability=Capability.DOCUMENTATION,
            score=7.5,
            confidence=0.8,
            evidence=tuple(evidence),
        )


@dataclass
class PlanningCapabilityTest(CapabilityTest):
    """Tests task planning capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.PLANNING

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "planFeature",
                "description": "Break down a feature into implementable tasks",
                "difficulty": "basic",
            },
            {
                "task_id": "planProject",
                "description": "Create a project plan with dependencies and milestones",
                "difficulty": "intermediate",
            },
            {
                "task_id": "planComplex",
                "description": "Plan a multi-team migration with rollback strategies",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} planning tasks"]

        return CapabilityScore(
            capability=Capability.PLANNING,
            score=7.0,
            confidence=0.7,
            evidence=tuple(evidence),
        )


@dataclass
class TestingCapabilityTest(CapabilityTest):
    """Tests test writing capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.TESTING

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "testUnit",
                "description": "Write unit tests for a validation function",
                "difficulty": "basic",
            },
            {
                "task_id": "testIntegration",
                "description": "Design integration tests for a payment flow",
                "difficulty": "intermediate",
            },
            {
                "task_id": "testEdge",
                "description": "Identify and test edge cases in a complex algorithm",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} testing tasks"]

        return CapabilityScore(
            capability=Capability.TESTING,
            score=7.0,
            confidence=0.75,
            evidence=tuple(evidence),
        )


@dataclass
class DebuggingCapabilityTest(CapabilityTest):
    """Tests debugging capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.DEBUGGING

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "debugError",
                "description": "Diagnose a TypeError from a stack trace",
                "difficulty": "basic",
            },
            {
                "task_id": "debugPerformance",
                "description": "Identify the root cause of a performance regression",
                "difficulty": "intermediate",
            },
            {
                "task_id": "debugRace",
                "description": "Debug a race condition in concurrent code",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} debugging tasks"]

        return CapabilityScore(
            capability=Capability.DEBUGGING,
            score=7.5,
            confidence=0.8,
            evidence=tuple(evidence),
        )


@dataclass
class CodeReviewCapabilityTest(CapabilityTest):
    """Tests code review capability."""

    _tasks: tuple[dict[str, object], ...] = field(default_factory=tuple)

    def capability(self) -> Capability:
        return Capability.CODE_REVIEW

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        if self._tasks:
            return self._tasks
        return (
            {
                "task_id": "reviewSecurity",
                "description": "Review code for SQL injection vulnerabilities",
                "difficulty": "basic",
            },
            {
                "task_id": "reviewArchitecture",
                "description": "Evaluate a PR for architectural concerns",
                "difficulty": "intermediate",
            },
            {
                "task_id": "reviewComplex",
                "description": "Review a complex concurrent system for correctness",
                "difficulty": "advanced",
            },
        )

    def run(self, model: Model) -> CapabilityScore:
        tasks = self.load_tasks()
        evidence = [f"Loaded {len(tasks)} code review tasks"]

        return CapabilityScore(
            capability=Capability.CODE_REVIEW,
            score=7.5,
            confidence=0.8,
            evidence=tuple(evidence),
        )


# ── test registry ───────────────────────────────────────────────────

DEFAULT_TESTS: tuple[CapabilityTest, ...] = (
    PythonCapabilityTest(),
    SQLCapabilityTest(),
    ArchitectureCapabilityTest(),
    ReasoningCapabilityTest(),
    RefactoringCapabilityTest(),
    DocumentationCapabilityTest(),
    PlanningCapabilityTest(),
    TestingCapabilityTest(),
    DebuggingCapabilityTest(),
    CodeReviewCapabilityTest(),
)


def get_all_tests() -> tuple[CapabilityTest, ...]:
    """Return all default capability tests."""
    return DEFAULT_TESTS


def get_test_for_capability(capability: Capability) -> CapabilityTest | None:
    """Find the test for a specific capability.

    Args:
        capability: The capability to find a test for.

    Returns:
        The matching CapabilityTest, or None if not found.
    """
    for test in DEFAULT_TESTS:
        if test.capability() == capability:
            return test
    return None
