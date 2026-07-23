from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from core.ids import AssetId
from core.models.asset_metadata import AssetMetadata, PromotionStatus


@runtime_checkable
class AssetProtocol(Protocol):
    """Protocol for assets that can be stored in an AssetRepository.

    Any asset type with an `id` and `metadata` property satisfies this protocol.
    """

    @property
    def id(self) -> AssetId: ...

    @property
    def metadata(self) -> AssetMetadata: ...


@runtime_checkable
class AssetRepository(Protocol):
    """Abstract repository for persisting and querying assets.

    Implementations handle storage (in-memory, file-based, database).
    Assets are stored and retrieved by their AssetId.
    """

    def store(self, asset: AssetProtocol) -> None:
        """Store an asset.

        Args:
            asset: Any asset implementing AssetProtocol (SkillAsset, PromptAsset, etc.)

        Raises:
            ValueError: If an asset with the same ID already exists.
        """

    def get(self, asset_id: AssetId) -> AssetProtocol | None:
        """Retrieve an asset by ID.

        Args:
            asset_id: The unique identifier of the asset.

        Returns:
            The asset if found, None otherwise.
        """

    def list_by_type(self, asset_type: type) -> tuple[AssetProtocol, ...]:
        """List all assets of a given type.

        Args:
            asset_type: The class type to filter by.

        Returns:
            Tuple of matching assets.
        """

    def list_by_status(self, status: PromotionStatus) -> tuple[AssetProtocol, ...]:
        """List all assets with a given promotion status.

        Args:
            status: The promotion status to filter by.

        Returns:
            Tuple of matching assets.
        """

    def update(self, asset: AssetProtocol) -> None:
        """Update an existing asset.

        Args:
            asset: The asset with updated fields.

        Raises:
            KeyError: If the asset ID does not exist.
        """

    def delete(self, asset_id: AssetId) -> None:
        """Delete an asset by ID.

        Args:
            asset_id: The unique identifier of the asset to delete.

        Raises:
            KeyError: If the asset ID does not exist.
        """

    def count(self) -> int:
        """Return the total number of stored assets."""
