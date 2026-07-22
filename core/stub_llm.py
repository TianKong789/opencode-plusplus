from __future__ import annotations

from dataclasses import dataclass

from core.interfaces.llm_executor import LLMExecutor


@dataclass(slots=True, frozen=True)
class StubLLMExecutor(LLMExecutor):
    """Stub LLM executor for testing and development.

    Returns configurable responses without making API calls.
    """

    response: str = ""

    def execute(self, prompt: str) -> str:
        return self.response
