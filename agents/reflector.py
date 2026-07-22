from __future__ import annotations

from dataclasses import dataclass, field

from core.events.reflection import ReflectionCompleted
from core.ids import EvaluationId, ReflectionId
from core.interfaces.event_bus import EventBus
from core.interfaces.reflector import Reflector
from core.models.evaluation import Evaluation
from core.models.reflection import Reflection
from core.null_objects import NullEventBus


@dataclass(slots=True, frozen=True)
class ReflectorAgent(Reflector):
    """Analyzes evaluations to extract insights and improvement actions.

    Placeholder implementation — replace with LLM-driven reflection
    for production use.
    """

    event_bus: EventBus = field(default_factory=NullEventBus)

    def reflect(self, evaluation: Evaluation) -> Reflection:
        insights: tuple[str, ...] = ()
        improvements: tuple[str, ...] = ()

        if evaluation.score < 1.0:
            insights = (f"Score was {evaluation.score}, not perfect.",)
            improvements = ("Retry with adjusted parameters.",)

        reflection = Reflection(
            id=ReflectionId(f"refl-{evaluation.id}"),
            evaluation_id=EvaluationId(evaluation.id),
            insights=insights,
            improvements=improvements,
            root_cause=evaluation.summary,
        )
        self.event_bus.publish(
            ReflectionCompleted(
                source="reflector",
                reflection_id=reflection.id,
                evaluation_id=evaluation.id,
                insight_count=len(reflection.insights),
            )
        )
        return reflection

    def get_reflection(self, reflection_id: str) -> Reflection | None:
        return None
