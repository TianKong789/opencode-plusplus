from benchmarks.metrics import MetricsTracker
from core.ids import EvaluationId, ExecutionId
from core.models.evaluation import Evaluation, Verdict


def _make_evaluation(
    ev_id: str = "ev1",
    score: float = 0.8,
    verdict: Verdict = Verdict.PASS,
) -> Evaluation:
    return Evaluation(
        id=EvaluationId(ev_id),
        execution_id=ExecutionId("ex1"),
        score=score,
        verdict=verdict,
        criteria=("quality",),
    )


class TestMetricsTracker:
    def test_empty_tracker(self) -> None:
        tracker = MetricsTracker()
        assert tracker.average_score() == 0.0
        assert tracker.pass_rate() == 0.0
        assert tracker.count() == 0

    def test_record_and_average(self) -> None:
        tracker = MetricsTracker()
        tracker.record(_make_evaluation(score=0.6))
        tracker.record(_make_evaluation(score=0.8))
        assert tracker.average_score() == 0.7
        assert tracker.count() == 2

    def test_pass_rate(self) -> None:
        tracker = MetricsTracker()
        tracker.record(_make_evaluation(verdict=Verdict.PASS))
        tracker.record(_make_evaluation(verdict=Verdict.FAIL))
        assert tracker.pass_rate() == 0.5

    def test_all_passing(self) -> None:
        tracker = MetricsTracker()
        tracker.record(_make_evaluation(verdict=Verdict.PASS))
        tracker.record(_make_evaluation(verdict=Verdict.PASS))
        assert tracker.pass_rate() == 1.0
