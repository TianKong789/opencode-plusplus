from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, unique

from core.ids import AssetId


@unique
class PromotionStatus(Enum):
    """Lifecycle states for assets.

    State diagram::

        DRAFT ──▶ APPROVED ──▶ PROMOTED
                       ──▶ ARCHIVED
    """

    DRAFT = "draft"
    APPROVED = "approved"
    PROMOTED = "promoted"
    ARCHIVED = "archived"


@dataclass(slots=True, frozen=True)
class AssetMetadata:
    """Reusable metadata for any versioned, persistent engineering artifact.

    Embedded in asset types via composition — not inherited.
    """

    asset_id: AssetId
    version: str = "0.1.0"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""
    parent: AssetId | None = None
    tags: tuple[str, ...] = ()
    provenance: str = ""
    lifecycle: PromotionStatus = PromotionStatus.DRAFT

    def __post_init__(self) -> None:
        if not self.asset_id:
            raise ValueError("AssetMetadata asset_id must not be empty")
        if not self.version:
            raise ValueError("AssetMetadata version must not be empty")

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    def is_approved(self) -> bool:
        return self.lifecycle == PromotionStatus.APPROVED

    def is_promoted(self) -> bool:
        return self.lifecycle == PromotionStatus.PROMOTED

    def is_archived(self) -> bool:
        return self.lifecycle == PromotionStatus.ARCHIVED
