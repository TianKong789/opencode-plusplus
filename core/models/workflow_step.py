"""Immutable domain model for a Workflow Step.

A WorkflowStep represents a single unit of work within a Workflow.
Each step has a type that determines what kind of executor handles it,
an optional condition for conditional execution, retry semantics,
and a timeout.

Steps are connected via the Workflow's step sequence and can reference
each other through conditions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from core.ids import WorkflowStepId


@unique
class StepType(Enum):
    """The kind of executor that handles a workflow step.

    Only ENGINE and SYSTEM are currently supported.  Additional step types
    (SKILL, AGENT, TOOL, HUMAN) are planned for future phases but must not
    be declared until a corresponding handler is implemented.
    """

    ENGINE = "engine"
    """Run through an execution engine (code execution)."""

    SYSTEM = "system"
    """Internal system operation (no external invocation)."""


@dataclass(slots=True, frozen=True)
class RetryPolicy:
    """Configuration for step retry behavior.

    Attributes:
        max_retries: Maximum number of retry attempts.  ``0`` means
            no retries (execute once).
        backoff_multiplier: Multiplier applied to the wait time between
            retries.  ``1.0`` means constant delay; ``2.0`` means
            exponential backoff.
    """

    max_retries: int = 0
    """Maximum number of retry attempts (default ``0`` = no retries)."""

    backoff_multiplier: float = 1.0
    """Multiplier for wait time between retries (default ``1.0``)."""

    def __post_init__(self) -> None:
        """Validate retry policy invariants."""
        if self.max_retries < 0:
            raise ValueError("RetryPolicy max_retries must not be negative")
        if self.backoff_multiplier < 0.0:
            raise ValueError("RetryPolicy backoff_multiplier must not be negative")


@dataclass(slots=True, frozen=True)
class WorkflowStep:
    """An immutable, validated step within a workflow.

    Each step defines what to execute, how to handle failures,
    and when to execute (condition).

    Attributes:
        id: Globally unique identifier.  Must be non-empty.
        name: Human-readable name for this step.  Must be non-empty.
        type: The kind of executor that handles this step.
        target: Identifier of the resource to invoke
            (skill name, agent type, tool ID, etc.).
        condition: Optional expression that determines whether this
            step executes.  ``None`` means unconditional execution.
        retry_policy: Configuration for retry behavior on failure.
        timeout: Maximum execution time in milliseconds.  ``0.0``
            means no timeout.
    """

    id: WorkflowStepId
    """Globally unique identifier (e.g. ``WorkflowStepId("step-abc")``)."""

    name: str
    """Human-readable name for this step."""

    type: StepType
    """The kind of executor that handles this step."""

    target: str
    """Identifier of the resource to invoke (skill, agent, tool, etc.)."""

    condition: str | None = None
    """Optional expression controlling conditional execution."""

    retry_policy: RetryPolicy = RetryPolicy()
    """Retry behavior on failure.  Defaults to no retries."""

    timeout: float = 0.0
    """Maximum execution time in milliseconds.  ``0.0`` = no timeout."""

    def __post_init__(self) -> None:
        """Validate invariants that cannot be enforced by the type system."""
        if not self.id:
            raise ValueError("WorkflowStep id must not be empty")
        if not self.name:
            raise ValueError("WorkflowStep name must not be empty")
        if not self.target:
            raise ValueError("WorkflowStep target must not be empty")
        if self.timeout < 0.0:
            raise ValueError("WorkflowStep timeout must not be negative")

    # ── query helpers ───────────────────────────────────────────────

    def has_condition(self) -> bool:
        """Check whether this step has a conditional expression.

        Returns:
            ``True`` if ``condition`` is not ``None``.
        """
        return self.condition is not None

    def has_retry(self) -> bool:
        """Check whether this step is configured to retry on failure.

        Returns:
            ``True`` if ``max_retries`` is greater than ``0``.
        """
        return self.retry_policy.max_retries > 0

    def has_timeout(self) -> bool:
        """Check whether this step has a timeout configured.

        Returns:
            ``True`` if ``timeout`` is greater than ``0.0``.
        """
        return self.timeout > 0.0
