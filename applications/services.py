from __future__ import annotations

from dataclasses import dataclass

from core.events.experience import ExperienceStored
from core.ids import ExperienceId
from core.interfaces.event_bus import EventBus
from core.interfaces.experience_store import ExperienceStore
from core.models.experience import Experience
from core.models.reflection import Reflection


@dataclass(slots=True, frozen=True)
class ExperienceCapture:
    """Converts reflections into durable experiences and publishes the result."""

    experience_store: ExperienceStore
    event_bus: EventBus

    def capture(self, reflection: Reflection) -> Experience:
        lesson = reflection.insights[0] if reflection.insights else reflection.root_cause
        context = reflection.root_cause or "; ".join(reflection.insights)

        experience = Experience(
            id=ExperienceId(f"exp-{reflection.id}"),
            reflection_id=reflection.id,
            lesson=lesson,
            context=context,
        )
        self.experience_store.store_experience(experience)
        self.event_bus.publish(
            ExperienceStored(
                source="experience_capture",
                experience_id=experience.id,
                reflection_id=reflection.id,
                lesson=experience.lesson,
            )
        )
        return experience
