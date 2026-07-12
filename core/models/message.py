from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique


@unique
class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(slots=True, frozen=True)
class Message:
    id: str
    role: MessageRole
    content: str
    parent_id: str | None = None

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Message id must not be empty")
        if not self.content:
            raise ValueError("Message content must not be empty")

    def is_root(self) -> bool:
        return self.parent_id is None
