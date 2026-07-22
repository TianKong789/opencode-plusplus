from __future__ import annotations

from dataclasses import dataclass

from core.ids import EvaluationId, ReflectionId
from core.interfaces.reflector import Reflector
from core.models.evaluation import Evaluation
from core.models.reflection import Reflection


@dataclass(slots=True, frozen=True)
class ReflectorAgent(Reflector):
    """Analyzes evaluations to extract insights and improvement actions.

    Placeholder implementation — replace with LLM-driven reflection
    for production use.
    """

    def reflect(self, evaluation: Evaluation) -> Reflection:
        insights: tuple[str, ...] = ()
        improvements: tuple[str, ...] = ()

        if evaluation.score < 1.0:
            insights = (f"Score was {evaluation.score}, not perfect.",)
            improvements = ("Retry with adjusted parameters.",)

        return Reflection(
            id=ReflectionId(f"refl-{evaluation.id}"),
            evaluation_id=EvaluationId(evaluation.id),
            insights=insights,
            improvements=improvements,
            root_cause=evaluation.summary,
        )

    def get_reflection(self, reflection_id: str) -> Reflection | None:
        return None
