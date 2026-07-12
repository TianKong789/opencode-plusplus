from __future__ import annotations


class ProjectError(Exception):
    """Base exception for all opencode++ errors."""


class PlanningError(ProjectError):
    """Raised when plan creation or approval fails."""


class ExecutionError(ProjectError):
    """Raised when plan execution or code running fails."""


class EvaluationError(ProjectError):
    """Raised when evaluation of an execution fails."""


class MemoryStoreError(ProjectError):
    """Raised when experience or skill storage fails."""


class EvolutionError(ProjectError):
    """Raised when the evolution loop encounters a failure."""


class SkillError(ProjectError):
    """Raised when a skill operation fails."""


class WorkspaceError(ProjectError):
    """Raised when a workspace operation fails."""
