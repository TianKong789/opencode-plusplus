from agents.reviewer import ReviewerAgent
from core.ids import ArtifactId, PlanId
from core.models.code_artifact import CodeArtifact
from core.models.review import ReviewVerdict


def _make_artifact(
    art_id: str = "a1",
    files: tuple[str, ...] = ("main.py",),
) -> CodeArtifact:
    return CodeArtifact(
        id=ArtifactId(art_id),
        plan_id=PlanId("p1"),
        files=files,
    )


class TestReviewerAgent:
    def test_review_approves_with_files(self) -> None:
        agent = ReviewerAgent()
        artifact = _make_artifact()
        review = agent.review(artifact)
        assert review.is_approved()
        assert review.score == 1.0
        assert review.verdict == ReviewVerdict.APPROVE

    def test_review_requests_changes_without_files(self) -> None:
        agent = ReviewerAgent()
        artifact = _make_artifact(files=())
        review = agent.review(artifact)
        assert not review.is_approved()
        assert review.score == 0.0
        assert review.verdict == ReviewVerdict.REQUEST_CHANGES
        assert len(review.findings) > 0

    def test_review_links_to_artifact(self) -> None:
        agent = ReviewerAgent()
        artifact = _make_artifact(art_id="art-42")
        review = agent.review(artifact)
        assert review.artifact_id == "art-42"

    def test_get_review_returns_none(self) -> None:
        agent = ReviewerAgent()
        assert agent.get_review("any") is None
