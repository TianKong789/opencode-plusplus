from __future__ import annotations

from dataclasses import dataclass

from core.events.experience import ExperienceStored
from core.ids import ExperienceId
from core.interfaces.event_bus import EventBus
from core.interfaces.memory_provider import MemoryProvider
from core.models.experience import Experience
from core.models.reflection import Reflection


@dataclass(slots=True, frozen=True)
class ExperienceCapture:
    """Converts Reflections into Experiences and persists them.

    This is a Runtime Service — a command that changes the world
    (stores experience) and emits an event describing what changed.
    """

    memory: MemoryProvider
    event_bus: EventBus

    def capture(self, reflection: Reflection) -> Experience:
        """Capture a reflection as a durable experience.

        Args:
            reflection: The reflection to capture.

        Returns:
            The stored experience.
        """
        lesson = reflection.insights[0] if reflection.insights else reflection.root_cause
        context = reflection.root_cause or "; ".join(reflection.insights)

        experience = Experience(
            id=ExperienceId(f"exp-{reflection.id}"),
            reflection_id=reflection.id,
            lesson=lesson,
            context=context,
        )
        self.memory.store_experience(experience)
        self.event_bus.publish(
            ExperienceStored(
                source="experience_capture",
                experience_id=experience.id,
                reflection_id=reflection.id,
                lesson=experience.lesson,
            )
        )
        return experience
