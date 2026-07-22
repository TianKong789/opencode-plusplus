from agents.tester import TesterAgent
from core.ids import ArtifactId, PlanId
from core.models.code_artifact import CodeArtifact
from core.models.test_result import TestVerdict


def _make_artifact(
    art_id: str = "a1",
    files: tuple[str, ...] = ("main.py",),
) -> CodeArtifact:
    return CodeArtifact(
        id=ArtifactId(art_id),
        plan_id=PlanId("p1"),
        files=files,
    )


class TestTesterAgent:
    def test_test_passes_with_files(self) -> None:
        agent = TesterAgent()
        artifact = _make_artifact()
        result = agent.test(artifact)
        assert result.is_passing()
        assert result.verdict == TestVerdict.PASS
        assert result.passed == 1
        assert result.failed == 0

    def test_test_fails_without_files(self) -> None:
        agent = TesterAgent()
        artifact = _make_artifact(files=())
        result = agent.test(artifact)
        assert not result.is_passing()
        assert result.verdict == TestVerdict.FAIL
        assert result.failed == 1
        assert len(result.errors) > 0

    def test_test_total(self) -> None:
        agent = TesterAgent()
        artifact = _make_artifact()
        result = agent.test(artifact)
        assert result.total() == 1

    def test_get_result_returns_none(self) -> None:
        agent = TesterAgent()
        assert agent.get_result("any") is None
