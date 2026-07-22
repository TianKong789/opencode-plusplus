from __future__ import annotations

from abc import ABC, abstractmethod

from core.ids import ModelId


class ModelRegistry(ABC):
    """Manages available models and their metadata.

    Provides a registry of LLMs known to the system, including
    their capabilities, costs, and operational status.
    """

    @abstractmethod
    def register(
        self,
        model_id: ModelId,
        name: str,
        provider: str,
        capabilities: tuple[str, ...] = (),
    ) -> None:
        """Register a new model in the registry.

        Args:
            model_id: Unique identifier for the model.
            name: Human-readable model name (e.g. "claude-sonnet-4-20250514").
            provider: The provider or vendor (e.g. "anthropic", "openai").
            capabilities: Capability tags (e.g. "code", "reasoning", "vision").
        """

    @abstractmethod
    def get(self, model_id: ModelId) -> dict[str, object] | None:
        """Retrieve model metadata by identifier.

        Args:
            model_id: The unique identifier of the model.

        Returns:
            A dictionary of model metadata, or None if not found.
        """

    @abstractmethod
    def list_models(self) -> tuple[ModelId, ...]:
        """List all registered model identifiers.

        Returns:
            A tuple of all registered model IDs.
        """

    @abstractmethod
    def list_by_capability(self, capability: str) -> tuple[ModelId, ...]:
        """List models that have a specific capability.

        Args:
            capability: The capability tag to filter by (e.g. "code").

        Returns:
            A tuple of model IDs with the specified capability.
        """

    @abstractmethod
    def remove(self, model_id: ModelId) -> None:
        """Remove a model from the registry.

        Args:
            model_id: The identifier of the model to remove.

        Raises:
            KeyError: If the model ID does not exist.
        """

    @abstractmethod
    def count(self) -> int:
        """Return the total number of registered models."""
