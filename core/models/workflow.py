"""Immutable domain model for a Workflow.

A Workflow defines an ordered sequence of steps that together accomplish
a complex engineering task.  Workflows are the primary unit of
composition in OpenCode++ — they wire together skills, agents, tools,
engines, and human gates into reproducible pipelines.

Workflows are versioned and support named inputs/outputs for
composability (one workflow's outputs can feed another's inputs).
"""

from __future__ import annotations

from dataclasses import dataclass

from core.ids import WorkflowId
from core.models.workflow_step import WorkflowStep


@dataclass(slots=True, frozen=True)
class Workflow:
    """An immutable, validated sequence of steps.

    All fields are set at construction time and cannot be modified.
    Use ``dataclasses.replace()`` to derive a new Workflow with changed
    fields (e.g. to advance version).

    Attributes:
        id: Globally unique identifier.  Must be non-empty.
        name: Short human-readable name.  Must be non-empty.
        description: Detailed explanation of what the workflow does.
        version: Semantic version string (e.g. ``"0.1.0"``).
        steps: Ordered sequence of steps to execute.
        inputs: Names of expected input parameters.
        outputs: Names of produced output artifacts.
        metadata: Arbitrary key-value metadata stored as an immutable
            tuple of pairs.  Use ``get_metadata()`` for dict access.
    """

    id: WorkflowId
    """Globally unique identifier (e.g. ``WorkflowId("wf-abc")``)."""

    name: str
    """Short human-readable name for this workflow."""

    description: str
    """Detailed explanation of what the workflow accomplishes."""

    version: str = "0.1.0"
    """Semantic version string."""

    steps: tuple[WorkflowStep, ...] = ()
    """Ordered sequence of steps to execute."""

    inputs: tuple[str, ...] = ()
    """Names of expected input parameters."""

    outputs: tuple[str, ...] = ()
    """Names of produced output artifacts."""

    metadata: tuple[tuple[str, str], ...] = ()
    """Arbitrary key-value metadata as immutable pairs."""

    def __post_init__(self) -> None:
        """Validate invariants that cannot be enforced by the type system."""
        if not self.id:
            raise ValueError("Workflow id must not be empty")
        if not self.name:
            raise ValueError("Workflow name must not be empty")
        if not self.version:
            raise ValueError("Workflow version must not be empty")

    # ── query helpers ───────────────────────────────────────────────

    def step_count(self) -> int:
        """Return the number of steps in this workflow.

        Returns:
            The total number of steps.
        """
        return len(self.steps)

    def has_inputs(self) -> bool:
        """Check whether this workflow expects input parameters.

        Returns:
            ``True`` if ``inputs`` is non-empty.
        """
        return len(self.inputs) > 0

    def has_outputs(self) -> bool:
        """Check whether this workflow produces output artifacts.

        Returns:
            ``True`` if ``outputs`` is non-empty.
        """
        return len(self.outputs) > 0

    def has_metadata(self) -> bool:
        """Check whether this workflow has any metadata entries.

        Returns:
            ``True`` if ``metadata`` is non-empty.
        """
        return len(self.metadata) > 0

    def get_metadata(self, key: str, default: str = "") -> str:
        """Retrieve a metadata value by key.

        Args:
            key: The metadata key to look up.
            default: Value to return if key is not found.

        Returns:
            The metadata value, or ``default`` if not present.
        """
        for k, v in self.metadata:
            if k == key:
                return v
        return default

    def find_step(self, step_id: str) -> WorkflowStep | None:
        """Find a step by its ID.

        Args:
            step_id: The step ID string to search for.

        Returns:
            The matching :class:`WorkflowStep`, or ``None`` if not found.
        """
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def find_step_by_name(self, name: str) -> WorkflowStep | None:
        """Find a step by its name.

        Args:
            name: The step name to search for.

        Returns:
            The matching :class:`WorkflowStep`, or ``None`` if not found.
        """
        for step in self.steps:
            if step.name == name:
                return step
        return None
