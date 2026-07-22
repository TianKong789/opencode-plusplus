from __future__ import annotations

from dataclasses import dataclass, replace

from core.assets.metadata import AssetMetadata, PromotionStatus
from core.ids import AssetId


@dataclass(slots=True, frozen=True)
class TemplateAsset:
    """A versioned, promotable template (workflow, review, evaluation criteria, etc.).

    Wraps template content with AssetMetadata for lifecycle management.
    """

    metadata: AssetMetadata
    name: str
    content: str
    template_type: str = "generic"

    def __post_init__(self) -> None:
        if not self.metadata:
            raise ValueError("TemplateAsset metadata must not be empty")
        if not self.name:
            raise ValueError("TemplateAsset name must not be empty")
        if not self.content:
            raise ValueError("TemplateAsset content must not be empty")

    @property
    def id(self) -> AssetId:
        return self.metadata.asset_id

    @property
    def version(self) -> str:
        return self.metadata.version

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TemplateAsset):
            return NotImplemented
        return self.metadata.asset_id == other.metadata.asset_id

    def __hash__(self) -> int:
        return hash(self.metadata.asset_id)

    def promote(self) -> TemplateAsset:
        new_metadata = replace(self.metadata, lifecycle=PromotionStatus.PROMOTED)
        return replace(self, metadata=new_metadata)

    def archive(self) -> TemplateAsset:
        new_metadata = replace(self.metadata, lifecycle=PromotionStatus.ARCHIVED)
        return replace(self, metadata=new_metadata)
