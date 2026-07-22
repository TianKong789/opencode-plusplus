from __future__ import annotations

from abc import ABC, abstractmethod

from core.ids import CapabilityId, ModelId


class CapabilityAssessor(ABC):
    """Assesses model capabilities against task requirements.

    Evaluates how well a given model can handle a specific task
    based on historical performance, benchmarks, and task characteristics.
    """

    @abstractmethod
    def assess(self, model_id: ModelId, task_description: str) -> float:
        """Assess how well a model can handle a task.

        Args:
            model_id: The model to assess.
            task_description: A description of the task requirements.

        Returns:
            A score between 0.0 and 1.0 indicating suitability.
        """

    @abstractmethod
    def get_capability(self, capability_id: CapabilityId) -> dict[str, object] | None:
        """Retrieve a capability profile by identifier.

        Args:
            capability_id: The unique identifier of the capability profile.

        Returns:
            The capability profile if found, None otherwise.
        """

    @abstractmethod
    def list_capabilities(self, model_id: ModelId) -> tuple[CapabilityId, ...]:
        """List all capability profiles for a model.

        Args:
            model_id: The model to list capabilities for.

        Returns:
            A tuple of capability profile IDs.
        """

    @abstractmethod
    def update_assessment(
        self,
        model_id: ModelId,
        task_description: str,
        actual_performance: float,
    ) -> None:
        """Update assessment based on actual task performance.

        Args:
            model_id: The model that was used.
            task_description: The task that was performed.
            actual_performance: The observed performance score (0.0 to 1.0).
        """
