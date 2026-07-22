from __future__ import annotations

from dataclasses import dataclass

from core.ids import ArtifactId
from core.interfaces.coder import Coder
from core.models.code_artifact import CodeArtifact
from core.models.plan import Plan


@dataclass(slots=True, frozen=True)
class CoderAgent(Coder):
    """Implements code from a plan.

    Placeholder implementation — replace with LLM-driven code
    generation for production use.
    """

    def implement(self, plan: Plan) -> CodeArtifact:
        """Implement a plan as a code artifact.

        Args:
            plan: The approved plan to implement.

        Returns:
            A code artifact with a single file stub.
        """
        file_name = f"{plan.task_id}.py"
        return CodeArtifact(
            id=ArtifactId(f"art-{plan.id}"),
            plan_id=plan.id,
            files=(file_name,),
            summary=f"Implemented plan: {plan.strategy}",
        )

    def get_artifact(self, artifact_id: str) -> CodeArtifact | None:
        """Retrieve an artifact by its identifier.

        Args:
            artifact_id: The unique identifier of the artifact.

        Returns:
            None — artifacts are not persisted in this implementation.
        """
        return None
