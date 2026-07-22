"""Immutable domain model for a Task.

A Task represents a discrete unit of work to be processed by the
OpenCode++ pipeline.  Tasks flow through the core loop:

    Task → Plan → Execute → Evaluate → Reflect → Experience

This module defines only the data structure.  Scheduling, persistence,
and lifecycle management live in other packages.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique

from core.ids import TaskId


@unique
class TaskStatus(Enum):
    """Lifecycle states a Task can occupy.

    State diagram::

        PENDING ──▶ IN_PROGRESS ──▶ COMPLETED
                                 ──▶ FAILED
                                 ──▶ CANCELLED

    ``PENDING`` is the initial state.  ``COMPLETED``, ``FAILED``,
    and ``CANCELLED`` are terminal — no further transitions are expected.
    """

    PENDING = "pending"
    """Task has been created but work has not started."""

    IN_PROGRESS = "in_progress"
    """Work is actively being performed on this task."""

    COMPLETED = "completed"
    """Task finished successfully (terminal)."""

    FAILED = "failed"
    """Task terminated due to an error (terminal)."""

    CANCELLED = "cancelled"
    """Task was deliberately abandoned (terminal)."""


@dataclass(slots=True, frozen=True)
class Task:
    """An immutable, validated unit of work.

    All fields are set at construction time and cannot be modified.
    Use ``dataclasses.replace()`` to derive a new Task with changed
    fields (e.g. to transition status).

    Attributes:
        id: Globally unique identifier.  Must be non-empty.
        title: Short human-readable summary.  Must be non-empty.
        description: Detailed explanation of what the task requires.
        status: Current lifecycle state.  Defaults to ``PENDING``.
        tags: Free-form labels for filtering and grouping.
            Stored as a tuple for immutability.
        priority: Ordering hint (lower = higher priority).  Defaults to 0.
        parent_id: Optional identifier of a parent task for sub-task
            hierarchies.  ``None`` means this is a root task.
    """

    id: TaskId
    """Globally unique identifier (e.g. ``TaskId("task-a1b2c3")``)."""

    title: str
    """Short human-readable summary of the work."""

    description: str
    """Detailed explanation of what the task requires."""

    status: TaskStatus = TaskStatus.PENDING
    """Current lifecycle state.  Starts as ``PENDING``."""

    tags: tuple[str, ...] = ()
    """Free-form labels for filtering and grouping."""

    priority: int = 0
    """Ordering hint — lower values indicate higher priority."""

    parent_id: TaskId | None = None
    """Identifier of a parent task, or ``None`` for root tasks."""

    def __post_init__(self) -> None:
        """Validate invariants that cannot be enforced by the type system."""
        if not self.id:
            raise ValueError("Task id must not be empty")
        if not self.title:
            raise ValueError("Task title must not be empty")
        if self.priority < 0:
            raise ValueError("Task priority must not be negative")

    # ── query helpers ───────────────────────────────────────────────

    def is_terminal(self) -> bool:
        """Check whether the task is in a terminal state.

        Returns:
            ``True`` if status is ``COMPLETED``, ``FAILED``, or
            ``CANCELLED``.
        """
        return self.status in (
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.CANCELLED,
        )

    def is_root(self) -> bool:
        """Check whether this is a root-level task (no parent).

        Returns:
            ``True`` if ``parent_id`` is ``None``.
        """
        return self.parent_id is None

    def has_tag(self, tag: str) -> bool:
        """Check whether a specific tag is present.

        Args:
            tag: The tag string to look for.

        Returns:
            ``True`` if ``tag`` is in ``self.tags``.
        """
        return tag in self.tags
