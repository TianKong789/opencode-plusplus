from __future__ import annotations

from dataclasses import dataclass

from core.ids import ReviewId
from core.interfaces.reviewer import Reviewer
from core.models.code_artifact import CodeArtifact
from core.models.review import Review, ReviewVerdict


@dataclass(slots=True, frozen=True)
class ReviewerAgent(Reviewer):
    """Reviews code artifacts for quality and correctness.

    Placeholder implementation — replace with LLM-driven code review
    for production use.
    """

    def review(self, artifact: CodeArtifact) -> Review:
        """Review a code artifact.

        Args:
            artifact: The code artifact to review.

        Returns:
            A review that approves if artifact has at least one file.
        """
        score = 1.0 if artifact.files else 0.0
        verdict = ReviewVerdict.APPROVE if score > 0 else ReviewVerdict.REQUEST_CHANGES
        findings: tuple[str, ...] = ()
        if not artifact.files:
            findings = ("No files in artifact.",)

        return Review(
            id=ReviewId(f"rev-{artifact.id}"),
            artifact_id=artifact.id,
            score=score,
            verdict=verdict,
            findings=findings,
        )

    def get_review(self, review_id: str) -> Review | None:
        """Retrieve a review by its identifier.

        Args:
            review_id: The unique identifier of the review.

        Returns:
            None — reviews are not persisted in this implementation.
        """
        return None
