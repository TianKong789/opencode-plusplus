from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMExecutor(Protocol):
    """Interface for executing LLM prompts.

    Implementations handle the actual API call to an LLM provider.
    """

    def execute(self, prompt: str) -> str:
        """Execute a prompt against the LLM.

        Args:
            prompt: The prompt to send.

        Returns:
            The LLM response text.
        """
