"""Typed identifiers for domain models.

Every domain entity has a distinct ID type that inherits from
``BaseEntityId`` (itself a ``str`` subclass).  This gives us:

* **Static safety** — mypy rejects ``PlanId`` where ``TaskId`` is expected.
* **Runtime checks** — ``isinstance(id, BaseEntityId)`` catches all IDs.
* **Zero friction** — IDs behave like plain strings (no ``.value`` access).

Usage::

    from core.ids import TaskId

    tid = TaskId("task-abc")
    assert isinstance(tid, str)       # True
    assert tid == "task-abc"          # True
"""

from __future__ import annotations


class BaseEntityId(str):
    """Base class for all typed domain identifiers.

    Inherits from ``str`` so IDs can be used anywhere a string is
    expected — f-prints, dict keys, concatenation, and so on.
    """

    def __new__(cls, value: str) -> BaseEntityId:
        """Create a new entity ID.

        Args:
            value: The underlying string identifier.

        Returns:
            A new ID instance.
        """
        return super().__new__(cls, value)


class TaskId(BaseEntityId):
    """Unique identifier for a :class:`core.models.task.Task`."""


class PlanId(BaseEntityId):
    """Unique identifier for a :class:`core.models.plan.Plan`."""


class ExecutionId(BaseEntityId):
    """Unique identifier for a :class:`core.models.execution.Execution`."""


class EvaluationId(BaseEntityId):
    """Unique identifier for a :class:`core.models.evaluation.Evaluation`."""


class ReflectionId(BaseEntityId):
    """Unique identifier for a :class:`core.models.reflection.Reflection`."""


class ExperienceId(BaseEntityId):
    """Unique identifier for a :class:`core.models.experience.Experience`."""


class SkillId(BaseEntityId):
    """Unique identifier for a :class:`core.models.skill.Skill`."""


class BenchmarkId(BaseEntityId):
    """Unique identifier for a :class:`core.models.benchmark.Benchmark`."""


class WorkspaceId(BaseEntityId):
    """Unique identifier for a :class:`core.models.workspace.Workspace`."""


class MessageId(BaseEntityId):
    """Unique identifier for a :class:`core.models.message.Message`."""


class WorkflowId(BaseEntityId):
    """Unique identifier for a :class:`core.models.workflow.Workflow`."""


class WorkflowStepId(BaseEntityId):
    """Unique identifier for a :class:`core.models.workflow_step.WorkflowStep`."""


class AssetId(BaseEntityId):
    """Unique identifier for an Asset (persistent, versioned artifact)."""


class ModelId(BaseEntityId):
    """Unique identifier for a model (LLM, embedding, etc.)."""


class CapabilityId(BaseEntityId):
    """Unique identifier for a model capability profile."""


class TaskCategoryId(BaseEntityId):
    """Unique identifier for a task category classification."""


class ArtifactId(BaseEntityId):
    """Unique identifier for a code artifact produced by a Coder agent."""


class ReviewId(BaseEntityId):
    """Unique identifier for a code review produced by a Reviewer agent."""


class TestResultId(BaseEntityId):
    """Unique identifier for test results produced by a Tester agent."""


class ResearchId(BaseEntityId):
    """Unique identifier for research findings produced by a Researcher agent."""
