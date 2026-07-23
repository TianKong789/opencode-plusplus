"""Protocol for persisting evolution results."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.evaluation import Evaluation
from core.models.skill import Skill


@runtime_checkable
class EvolutionPersistence(Protocol):
    """Persist evolved skills and evaluation outcomes."""

    def persist(self, skills: tuple[Skill, ...], evaluation: Evaluation) -> None: ...
