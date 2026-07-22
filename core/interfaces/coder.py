from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.code_artifact import CodeArtifact
from core.models.plan import Plan


class Coder(ABC):
    """Implements code from a plan."""

    @abstractmethod
    def implement(self, plan: Plan) -> CodeArtifact:
        """Implement a plan as code.

        Args:
            plan: The approved plan to implement.

        Returns:
            A code artifact containing the generated files.
        """

    @abstractmethod
    def get_artifact(self, artifact_id: str) -> CodeArtifact | None:
        """Retrieve an artifact by its identifier.

        Args:
            artifact_id: The unique identifier of the artifact.

        Returns:
            The artifact if found, None otherwise.
        """
