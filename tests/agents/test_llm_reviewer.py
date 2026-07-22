from agents.llm_reviewer import LLMReviewerAgent
from core.ids import ArtifactId, PlanId
from core.models.code_artifact import CodeArtifact
from core.stub_llm import StubLLMExecutor


def _make_artifact(art_id: str = "a1") -> CodeArtifact:
    return CodeArtifact(
        id=ArtifactId(art_id),
        plan_id=PlanId("p1"),
        files=("main.py",),
    )


class TestLLMReviewerAgent:
    def test_review_uses_llm(self) -> None:
        llm = StubLLMExecutor(response="looks good")
        agent = LLMReviewerAgent(llm=llm)
        artifact = _make_artifact()
        review = agent.review(artifact)
        assert review.is_approved()
        assert "looks good" in review.findings[0]
