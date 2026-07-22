from __future__ import annotations

from dataclasses import dataclass, field

from core.events.evaluation import EvaluationCompleted
from core.ids import EvaluationId, ExecutionId
from core.interfaces.evaluator import Evaluator
from core.interfaces.event_bus import EventBus
from core.models.evaluation import Evaluation, Verdict
from core.models.execution import Execution
from core.null_objects import NullEventBus


@dataclass(slots=True, frozen=True)
class LLMEvaluator(Evaluator):
    """Evaluates execution results using heuristic scoring.

    Stores evaluations for retrieval by ID.
    """

    event_bus: EventBus = field(default_factory=NullEventBus)
    _evaluations: dict[str, Evaluation] = field(default_factory=dict, init=False, repr=False)

    def evaluate(self, execution: Execution) -> Evaluation:
        if execution.succeeded():
            score = 1.0 if execution.outputs else 0.5
            verdict = Verdict.PASS
        else:
            score = 0.0
            verdict = Verdict.FAIL

        evaluation = Evaluation(
            id=EvaluationId(f"eval-{execution.id}"),
            execution_id=ExecutionId(execution.id),
            score=score,
            verdict=verdict,
            criteria=("success",),
            summary=execution.error or "Execution completed",
        )
        self._evaluations[evaluation.id] = evaluation
        self.event_bus.publish(
            EvaluationCompleted(
                source="evaluator",
                evaluation_id=evaluation.id,
                execution_id=execution.id,
                score=evaluation.score,
                verdict=evaluation.verdict.value,
            )
        )
        return evaluation

    def get_evaluation(self, evaluation_id: str) -> Evaluation | None:
        return self._evaluations.get(evaluation_id)
