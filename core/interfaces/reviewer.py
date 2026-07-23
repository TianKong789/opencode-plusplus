from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.code_artifact import CodeArtifact
from core.models.review import Review


@runtime_checkable
class Reviewer(Protocol):
    """Reviews code artifacts for quality and correctness."""

    def review(self, artifact: CodeArtifact) -> Review:
        """Review a code artifact.

        Args:
            artifact: The code artifact to review.

        Returns:
            A review with score, verdict, and findings.
        """

    def get_review(self, review_id: str) -> Review | None:
        """Retrieve a review by its identifier.

        Args:
            review_id: The unique identifier of the review.

        Returns:
            The review if found, None otherwise.
        """
