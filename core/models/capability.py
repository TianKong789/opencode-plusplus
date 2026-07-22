"""Shared capability taxonomy for model assessment."""

from __future__ import annotations

from enum import Enum, unique


@unique
class Capability(Enum):
    """Capabilities that models can be assessed against."""

    PYTHON = "python"
    SQL = "sql"
    ORACLE_SQL = "oracle_sql"
    POSTGRES_SQL = "postgres_sql"
    ARCHITECTURE = "architecture"
    CODE_REVIEW = "code_review"
    DEBUGGING = "debugging"
    TESTING = "testing"
    REFACTORING = "refactoring"
    PLANNING = "planning"
    REASONING = "reasoning"
    PROMPT_ENGINEERING = "prompt_engineering"
    TOOL_USE = "tool_use"
    FUNCTION_CALLING = "function_calling"
    MULTIMODAL = "multimodal"
    MATH = "math"
    WRITING = "writing"
    DOCUMENTATION = "documentation"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"

    @classmethod
    def from_string(cls, value: str) -> Capability:
        """Look up a capability by its string value."""
        try:
            return cls(value)
        except ValueError:
            valid = ", ".join(capability.value for capability in cls)
            raise ValueError(f"Unknown capability: {value!r}. Valid: {valid}")

    @classmethod
    def programming_languages(cls) -> tuple[Capability, ...]:
        """Return all programming language capabilities."""
        return (cls.PYTHON, cls.SQL, cls.ORACLE_SQL, cls.POSTGRES_SQL)

    @classmethod
    def software_engineering(cls) -> tuple[Capability, ...]:
        """Return all software engineering capabilities."""
        return (
            cls.ARCHITECTURE,
            cls.CODE_REVIEW,
            cls.DEBUGGING,
            cls.TESTING,
            cls.REFACTORING,
            cls.PLANNING,
            cls.REASONING,
        )

    @classmethod
    def ai_specific(cls) -> tuple[Capability, ...]:
        """Return all AI/ML-specific capabilities."""
        return (
            cls.PROMPT_ENGINEERING,
            cls.TOOL_USE,
            cls.FUNCTION_CALLING,
            cls.MULTIMODAL,
        )

    @classmethod
    def general(cls) -> tuple[Capability, ...]:
        """Return all general-purpose capabilities."""
        return (
            cls.MATH,
            cls.WRITING,
            cls.DOCUMENTATION,
            cls.SUMMARIZATION,
            cls.TRANSLATION,
        )
