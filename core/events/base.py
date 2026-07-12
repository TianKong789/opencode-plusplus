from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class BaseEvent:
    """Base class for all domain events.

    Attributes:
        id: Unique event identifier.
        source: The component that emitted this event.
        timestamp: Unix epoch in seconds when the event was created.
    """

    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    source: str = ""
    timestamp: float = field(default_factory=time.time)
