from __future__ import annotations

from dataclasses import dataclass, replace

from core.assets.metadata import AssetMetadata, PromotionStatus
from core.ids import AssetId


@dataclass(slots=True, frozen=True)
class PromptAsset:
    """A versioned, promotable prompt template.

    Wraps prompt text with AssetMetadata for lifecycle management.
    """

    metadata: AssetMetadata
    prompt: str
    description: str = ""

    def __post_init__(self) -> None:
        if not self.metadata:
            raise ValueError("PromptAsset metadata must not be empty")
        if not self.prompt:
            raise ValueError("PromptAsset prompt must not be empty")

    @property
    def id(self) -> AssetId:
        return self.metadata.asset_id

    @property
    def version(self) -> str:
        return self.metadata.version

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PromptAsset):
            return NotImplemented
        return self.metadata.asset_id == other.metadata.asset_id

    def __hash__(self) -> int:
        return hash(self.metadata.asset_id)

    def promote(self) -> PromptAsset:
        new_metadata = replace(self.metadata, lifecycle=PromotionStatus.PROMOTED)
        return replace(self, metadata=new_metadata)

    def archive(self) -> PromptAsset:
        new_metadata = replace(self.metadata, lifecycle=PromotionStatus.ARCHIVED)
        return replace(self, metadata=new_metadata)
