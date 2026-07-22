from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BaseAgent:
    """Shared base for all agent implementations.

    Provides common identification fields without imposing
    interface constraints — concrete agents inherit from
    their respective ABCs in addition to this base.
    """

    name: str = "agent"
    description: str = ""
