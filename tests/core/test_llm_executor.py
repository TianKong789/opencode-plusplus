from core.interfaces.llm_executor import LLMExecutor
from tests.support.stub_llm import StubLLMExecutor


class TestStubLLMExecutor:
    def test_execute_returns_configured_response(self) -> None:
        llm = StubLLMExecutor(response="hello")
        assert llm.execute("any prompt") == "hello"

    def test_execute_empty_response(self) -> None:
        llm = StubLLMExecutor()
        assert llm.execute("prompt") == ""
