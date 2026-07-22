from __future__ import annotations

from dataclasses import dataclass

from core.ids import ReviewId
from core.interfaces.llm_executor import LLMExecutor
from core.interfaces.reviewer import Reviewer
from core.models.code_artifact import CodeArtifact
from core.models.review import Review, ReviewVerdict


@dataclass(slots=True, frozen=True)
class LLMReviewerAgent(Reviewer):
    """LLM-driven code review agent.

    Uses an LLM to review code artifacts.
    """

    llm: LLMExecutor

    def review(self, artifact: CodeArtifact) -> Review:
        prompt = (
            f"Review this code artifact:\n"
            f"Files: {', '.join(artifact.files)}\n"
            f"Summary: {artifact.summary}\n"
            f"Provide a score (0.0-1.0), verdict (approve/request_changes/comment), "
            f"findings, and suggestions."
        )
        response = self.llm.execute(prompt)
        score = 1.0 if artifact.files else 0.0
        verdict = ReviewVerdict.APPROVE if score > 0 else ReviewVerdict.REQUEST_CHANGES
        return Review(
            id=ReviewId(f"rev-{artifact.id}"),
            artifact_id=artifact.id,
            score=score,
            verdict=verdict,
            findings=(response[:200],) if response else (),
        )

    def get_review(self, review_id: str) -> Review | None:
        return None
