from __future__ import annotations

from abc import ABC, abstractmethod


class LLMExecutor(ABC):
    """Interface for executing LLM prompts.

    Implementations handle the actual API call to an LLM provider.
    """

    @abstractmethod
    def execute(self, prompt: str) -> str:
        """Execute a prompt against the LLM.

        Args:
            prompt: The prompt to send.

        Returns:
            The LLM response text.
        """
