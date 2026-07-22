from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from core.events.base import BaseEvent
from core.interfaces.event_bus import EventBus


@dataclass(slots=True, frozen=True)
class NullEventBus(EventBus):
    """No-op event bus that discards all events.

    Use when event publication is not needed (tests, development stubs).
    Lives in ``core/`` so all layers can use it without cross-layer imports.
    """

    def publish(self, event: BaseEvent) -> None:
        """Discard the event (no-op).

        Args:
            event: The domain event (ignored).
        """

    def subscribe(self, event_type: type[BaseEvent], handler: Callable[[BaseEvent], None]) -> None:
        """Register a handler (silently ignored — events are never dispatched).

        Args:
            event_type: The event class to listen for.
            handler: Callback (never invoked).
        """
