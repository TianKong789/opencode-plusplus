from __future__ import annotations

from dataclasses import dataclass, replace

from core.assets.metadata import AssetMetadata, PromotionStatus
from core.ids import AssetId
from core.models.workflow import Workflow


@dataclass(slots=True, frozen=True)
class WorkflowAsset:
    """A versioned, promotable engineering workflow.

    Wraps a Workflow domain object with AssetMetadata for lifecycle management.
    """

    metadata: AssetMetadata
    content: Workflow

    def __post_init__(self) -> None:
        if not self.metadata:
            raise ValueError("WorkflowAsset metadata must not be empty")
        if not self.content:
            raise ValueError("WorkflowAsset content must not be empty")

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
        if not isinstance(other, WorkflowAsset):
            return NotImplemented
        return self.metadata.asset_id == other.metadata.asset_id

    def __hash__(self) -> int:
        return hash(self.metadata.asset_id)

    def promote(self) -> WorkflowAsset:
        new_metadata = replace(self.metadata, lifecycle=PromotionStatus.PROMOTED)
        return replace(self, metadata=new_metadata)

    def archive(self) -> WorkflowAsset:
        new_metadata = replace(self.metadata, lifecycle=PromotionStatus.ARCHIVED)
        return replace(self, metadata=new_metadata)
