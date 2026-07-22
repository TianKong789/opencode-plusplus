from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class AssetPromoted(BaseEvent):
    """Emitted when an experimental asset is promoted to production."""

    asset_type: str = ""
    asset_id: str = ""
    from_version: str = ""
    to_version: str = ""
