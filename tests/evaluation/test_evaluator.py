from core.ids import ExecutionId, PlanId
from core.models.execution import Execution, ExecutionStatus
from evaluation.evaluator import LLMEvaluator


def test_evaluate_successful_execution() -> None:
    evaluator = LLMEvaluator()
    execution = Execution(
        id=ExecutionId("e1"),
        plan_id=PlanId("p1"),
        status=ExecutionStatus.COMPLETED,
        outputs=("result",),
    )
    evaluation = evaluator.evaluate(execution)
    assert evaluation.score == 1.0
    assert evaluation.is_passing() is True


def test_evaluate_failed_execution() -> None:
    evaluator = LLMEvaluator()
    execution = Execution(
        id=ExecutionId("e2"),
        plan_id=PlanId("p1"),
        status=ExecutionStatus.FAILED,
        error="oops",
    )
    evaluation = evaluator.evaluate(execution)
    assert evaluation.score == 0.0
    assert evaluation.is_passing() is False
