"""Capability taxonomy for model assessment.

Defines the set of capabilities that can be evaluated and matched
against task requirements. Each capability represents a distinct
skill or domain that a model may excel at.
"""

from __future__ import annotations

from enum import Enum, unique


@unique
class Capability(Enum):
    """Capabilities that models can be assessed against.

    Each value represents a distinct skill domain. Use these instead
    of raw strings to ensure type safety and prevent typos.
    """

    # ── programming languages ────────────────────────────────────────

    PYTHON = "python"
    """Python coding and scripting."""

    SQL = "sql"
    """General SQL query writing."""

    ORACLE_SQL = "oracle_sql"
    """Oracle-specific SQL and PL/SQL."""

    POSTGRES_SQL = "postgres_sql"
    """PostgreSQL-specific SQL and extensions."""

    # ── software engineering ─────────────────────────────────────────

    ARCHITECTURE = "architecture"
    """System design and architectural decisions."""

    CODE_REVIEW = "code_review"
    """Analyzing code for quality, security, and correctness."""

    DEBUGGING = "debugging"
    """Diagnosing and fixing software defects."""

    TESTING = "testing"
    """Writing and running test suites."""

    REFACTORING = "refactoring"
    """Improving code structure without changing behavior."""

    PLANNING = "planning"
    """Breaking down tasks into executable steps."""

    REASONING = "reasoning"
    """Logical reasoning and problem-solving."""

    # ── AI/ML specific ───────────────────────────────────────────────

    PROMPT_ENGINEERING = "prompt_engineering"
    """Designing effective LLM prompts."""

    TOOL_USE = "tool_use"
    """Using external tools and APIs effectively."""

    FUNCTION_CALLING = "function_calling"
    """Generating structured function calls."""

    MULTIMODAL = "multimodal"
    """Processing images, audio, and other modalities."""

    # ── general capabilities ─────────────────────────────────────────

    MATH = "math"
    """Mathematical computation and reasoning."""

    WRITING = "writing"
    """Prose writing and content creation."""

    DOCUMENTATION = "documentation"
    """Technical documentation generation."""

    SUMMARIZATION = "summarization"
    """Condensing text into key points."""

    TRANSLATION = "translation"
    """Translating between natural languages."""

    # ── query helpers ────────────────────────────────────────────────

    @classmethod
    def from_string(cls, value: str) -> Capability:
        """Look up a capability by its string value.

        Args:
            value: The capability string (e.g. "python", "sql").

        Returns:
            The matching Capability enum member.

        Raises:
            ValueError: If the value is not a valid capability.
        """
        try:
            return cls(value)
        except ValueError:
            valid = ", ".join(c.value for c in cls)
            raise ValueError(f"Unknown capability: {value!r}. Valid: {valid}")

    @classmethod
    def programming_languages(cls) -> tuple[Capability, ...]:
        """Return all programming language capabilities.

        Returns:
            Tuple of language capabilities (PYTHON, SQL, etc.).
        """
        return (cls.PYTHON, cls.SQL, cls.ORACLE_SQL, cls.POSTGRES_SQL)

    @classmethod
    def software_engineering(cls) -> tuple[Capability, ...]:
        """Return all software engineering capabilities.

        Returns:
            Tuple of SE capabilities (ARCHITECTURE, DEBUGGING, etc.).
        """
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
        """Return all AI/ML-specific capabilities.

        Returns:
            Tuple of AI capabilities (PROMPT_ENGINEERING, TOOL_USE, etc.).
        """
        return (
            cls.PROMPT_ENGINEERING,
            cls.TOOL_USE,
            cls.FUNCTION_CALLING,
            cls.MULTIMODAL,
        )

    @classmethod
    def general(cls) -> tuple[Capability, ...]:
        """Return all general-purpose capabilities.

        Returns:
            Tuple of general capabilities (MATH, WRITING, etc.).
        """
        return (
            cls.MATH,
            cls.WRITING,
            cls.DOCUMENTATION,
            cls.SUMMARIZATION,
            cls.TRANSLATION,
        )
