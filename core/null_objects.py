from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from core.events.base import BaseEvent
from core.interfaces.event_bus import EventBus
from core.interfaces.experience_store import ExperienceStore
from core.interfaces.reflection_repository import ReflectionRepository
from core.interfaces.skill_repository import SkillRepository
from core.models.experience import Experience
from core.models.reflection import Reflection
from core.models.skill import Skill


@dataclass(slots=True, frozen=True)
class NullEventBus(EventBus):
    """No-op event bus that discards all events.

    Use when event publication is not needed (tests, development stubs).
    Lives in ``core/`` so all layers can use it without cross-layer imports.
    """

    def publish(self, event: BaseEvent) -> None:
        """Discard the event (no-op).

        Args:
            event: The domain event (ignored).
        """

    def subscribe(self, event_type: type[BaseEvent], handler: Callable[[BaseEvent], None]) -> None:
        """Register a handler (silently ignored — events are never dispatched).

        Args:
            event_type: The event class to listen for.
            handler: Callback (never invoked).
        """


@dataclass(slots=True, frozen=True)
class NullSkillRepository(SkillRepository):
    """No-op skill repository that discards all saves.

    Use when skill persistence is not needed (tests, development stubs).
    """

    def save(self, skill: Skill) -> None:
        """Discard the skill (no-op)."""

    def get(self, skill_id: str) -> Skill | None:
        """Always returns None."""

    def find_by_name(self, name: str) -> Skill | None:
        """Always returns None."""

    def list_all(self) -> tuple[Skill, ...]:
        """Return empty tuple."""

    def delete(self, skill_id: str) -> None:
        """No-op (nothing to delete)."""


@dataclass(slots=True, frozen=True)
class NullReflectionRepository(ReflectionRepository):
    """No-op reflection repository that discards all saves.

    Use when reflection persistence is not needed (tests, development stubs).
    """

    def save(self, reflection: Reflection) -> None:
        """Discard the reflection (no-op)."""

    def get(self, reflection_id: str) -> Reflection | None:
        """Always returns None."""

    def find_by_evaluation(self, evaluation_id: str) -> Reflection | None:
        """Always returns None."""

    def list_all(self) -> tuple[Reflection, ...]:
        """Return empty tuple."""

    def search(self, query: str) -> tuple[Reflection, ...]:
        """Return empty tuple."""

    def delete(self, reflection_id: str) -> None:
        """No-op (nothing to delete)."""


@dataclass(slots=True, frozen=True)
class NullExperienceStore(ExperienceStore):
    """No-op experience store that discards all experiences.

    Use when experience persistence is not needed (tests, development stubs).
    """

    def store_experience(self, experience: Experience) -> None:
        """Discard the experience (no-op)."""

    def get_experience(self, experience_id: str) -> Experience | None:
        """Always returns None."""

    def list_experiences(self) -> tuple[Experience, ...]:
        """Return empty tuple."""
