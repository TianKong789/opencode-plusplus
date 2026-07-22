from agents.llm_tester import LLMTesterAgent
from core.ids import ArtifactId, PlanId
from core.models.code_artifact import CodeArtifact
from core.stub_llm import StubLLMExecutor


def _make_artifact(art_id: str = "a1") -> CodeArtifact:
    return CodeArtifact(
        id=ArtifactId(art_id),
        plan_id=PlanId("p1"),
        files=("main.py",),
    )


class TestLLMTesterAgent:
    def test_test_uses_llm(self) -> None:
        llm = StubLLMExecutor(response="all tests pass")
        agent = LLMTesterAgent(llm=llm)
        artifact = _make_artifact()
        result = agent.test(artifact)
        assert result.is_passing()
        assert "all tests pass" in result.summary
