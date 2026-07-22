from __future__ import annotations

from core.models import Capability
from src.opencode.evaluation.capability.pipeline import AssessmentPipeline
from src.opencode.evaluation.capability.test_runner import TestSuiteResult


def test_assess_model_runs_the_five_stages_in_order(monkeypatch) -> None:
    pipeline = AssessmentPipeline()
    pipeline.register_model("model-1", "Model One", "provider")
    stages: list[str] = []
    final_profile = object()

    def load(capabilities: tuple[Capability, ...]):
        stages.append("load")
        return capabilities

    def execute(model_id: str, loaded, executor):
        stages.append("execute")
        return loaded

    def score(model_id: str, results):
        stages.append("score")
        return results

    def filter(scores):
        stages.append("filter")
        return scores

    def rank(model_id: str, scores):
        stages.append("rank")
        return final_profile

    monkeypatch.setattr(pipeline, "load", load, raising=False)
    monkeypatch.setattr(pipeline, "execute", execute, raising=False)
    monkeypatch.setattr(pipeline, "score", score, raising=False)
    monkeypatch.setattr(pipeline, "filter", filter, raising=False)
    monkeypatch.setattr(pipeline, "rank", rank, raising=False)

    profile = pipeline.assess_model(
        "model-1",
        executor=lambda model_id, task_input: task_input,
        capabilities=(Capability.PYTHON,),
    )

    assert stages == ["load", "execute", "score", "filter", "rank"]
    assert profile is final_profile


def test_rank_builds_profile_from_scores_that_meet_quality_threshold() -> None:
    pipeline = AssessmentPipeline()
    pipeline.register_model("model-1", "Model One", "provider")
    execution_results = (
        (
            Capability.PYTHON,
            TestSuiteResult(capability="python", average_score=1.0),
        ),
        (
            Capability.SQL,
            TestSuiteResult(capability="sql", average_score=0.6),
        ),
    )

    scores = pipeline.score("model-1", execution_results)
    profile = pipeline.rank("model-1", pipeline.filter(scores))

    assert tuple(score.capability for score in profile.capability_scores) == (
        Capability.PYTHON,
    )
    assert profile.overall_score == 10.0
