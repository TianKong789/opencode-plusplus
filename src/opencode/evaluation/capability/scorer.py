"""Scoring engine for capability assessments.

Evaluates test outputs against expected results and computes
capability scores.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique


@unique
class ScoreType(Enum):
    """Types of scoring methods."""

    EXACT_MATCH = "exact_match"
    """Exact string matching."""

    CONTAINS = "contains"
    """Check if output contains expected substring."""

    SEMANTIC = "semantic"
    """Semantic similarity scoring."""

    CUSTOM = "custom"
    """Custom scoring function."""
