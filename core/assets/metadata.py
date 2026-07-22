"""Asset metadata — re-exported from core domain for backwards compatibility."""

from core.ids import AssetId
from core.models.asset_metadata import AssetMetadata, PromotionStatus

__all__ = ["AssetId", "AssetMetadata", "PromotionStatus"]
