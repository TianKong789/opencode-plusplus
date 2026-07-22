from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.code_artifact import CodeArtifact
from core.models.review import Review


class Reviewer(ABC):
    """Reviews code artifacts for quality and correctness."""

    @abstractmethod
    def review(self, artifact: CodeArtifact) -> Review:
        """Review a code artifact.

        Args:
            artifact: The code artifact to review.

        Returns:
            A review with score, verdict, and findings.
        """

    @abstractmethod
    def get_review(self, review_id: str) -> Review | None:
        """Retrieve a review by its identifier.

        Args:
            review_id: The unique identifier of the review.

        Returns:
            The review if found, None otherwise.
        """
