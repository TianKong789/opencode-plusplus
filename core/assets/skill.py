from __future__ import annotations

from dataclasses import dataclass, replace

from core.assets.metadata import AssetMetadata, PromotionStatus
from core.ids import AssetId
from core.models.skill import Skill


@dataclass(slots=True, frozen=True)
class SkillAsset:
    """A versioned, promotable engineering skill.

    Wraps a Skill domain object with AssetMetadata for lifecycle management.
    """

    metadata: AssetMetadata
    content: Skill

    def __post_init__(self) -> None:
        if not self.metadata:
            raise ValueError("SkillAsset metadata must not be empty")
        if not self.content:
            raise ValueError("SkillAsset content must not be empty")

    @property
    def id(self) -> AssetId:
        return self.metadata.asset_id

    @property
    def version(self) -> str:
        return self.metadata.version

    @property
    def name(self) -> str:
        return self.content.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SkillAsset):
            return NotImplemented
        return self.metadata.asset_id == other.metadata.asset_id

    def __hash__(self) -> int:
        return hash(self.metadata.asset_id)

    def promote(self) -> SkillAsset:
        new_metadata = replace(self.metadata, lifecycle=PromotionStatus.PROMOTED)
        return replace(self, metadata=new_metadata)

    def archive(self) -> SkillAsset:
        new_metadata = replace(self.metadata, lifecycle=PromotionStatus.ARCHIVED)
        return replace(self, metadata=new_metadata)
