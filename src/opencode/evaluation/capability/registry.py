"""Model registry implementation.

Manages available models and their metadata, providing lookup
and filtering capabilities for model selection.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.ids import ModelId


@dataclass
class ModelRegistry:
    """Registry of available models and their metadata.

    Stores model information and provides efficient lookup by
    ID, capability, and other attributes.
    """

    _models: dict[ModelId, dict[str, object]] = field(default_factory=dict)

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
            name: Human-readable model name.
            provider: The provider or vendor.
            capabilities: Capability tags.
        """
        self._models[model_id] = {
            "name": name,
            "provider": provider,
            "capabilities": capabilities,
        }

    def get(self, model_id: ModelId) -> dict[str, object] | None:
        """Retrieve model metadata by identifier.

        Args:
            model_id: The unique identifier of the model.

        Returns:
            A dictionary of model metadata, or None if not found.
        """
        return self._models.get(model_id)

    def list_models(self) -> tuple[ModelId, ...]:
        """List all registered model identifiers.

        Returns:
            A tuple of all registered model IDs.
        """
        return tuple(self._models.keys())

    def list_by_capability(self, capability: str) -> tuple[ModelId, ...]:
        """List models that have a specific capability.

        Args:
            capability: The capability tag to filter by.

        Returns:
            A tuple of model IDs with the specified capability.
        """
        return tuple(
            model_id
            for model_id, metadata in self._models.items()
            if capability in metadata.get("capabilities", ())
        )

    def remove(self, model_id: ModelId) -> None:
        """Remove a model from the registry.

        Args:
            model_id: The identifier of the model to remove.

        Raises:
            KeyError: If the model ID does not exist.
        """
        if model_id not in self._models:
            raise KeyError(f"Model {model_id} not found")
        del self._models[model_id]

    def count(self) -> int:
        """Return the total number of registered models."""
        return len(self._models)
