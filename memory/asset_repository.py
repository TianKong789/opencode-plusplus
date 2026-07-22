from __future__ import annotations

from core.assets.metadata import AssetId, PromotionStatus
from core.interfaces.asset_repository import AssetProtocol, AssetRepository


class InMemoryAssetRepository(AssetRepository):
    """In-memory implementation of AssetRepository for testing and development."""

    def __init__(self) -> None:
        self._assets: dict[AssetId, AssetProtocol] = {}

    def store(self, asset: AssetProtocol) -> None:
        asset_id = asset.id
        if asset_id in self._assets:
            raise ValueError(f"Asset {asset_id} already exists")
        self._assets[asset_id] = asset

    def get(self, asset_id: AssetId) -> AssetProtocol | None:
        return self._assets.get(asset_id)

    def list_by_type(self, asset_type: type) -> tuple[AssetProtocol, ...]:
        return tuple(a for a in self._assets.values() if isinstance(a, asset_type))

    def list_by_status(self, status: PromotionStatus) -> tuple[AssetProtocol, ...]:
        return tuple(
            a for a in self._assets.values()
            if a.metadata.lifecycle == status
        )

    def update(self, asset: AssetProtocol) -> None:
        asset_id = asset.id
        if asset_id not in self._assets:
            raise KeyError(f"Asset {asset_id} not found")
        self._assets[asset_id] = asset

    def delete(self, asset_id: AssetId) -> None:
        if asset_id not in self._assets:
            raise KeyError(f"Asset {asset_id} not found")
        del self._assets[asset_id]

    def count(self) -> int:
        return len(self._assets)
