from evolution.prompt_evolver import PromptEvolver


class TestPromptEvolver:
    def test_mutate_appends_feedback(self) -> None:
        evolver = PromptEvolver()
        result = evolver.mutate("prompt", "needs more context")
        assert "needs more context" in result
        assert result.startswith("prompt")

    def test_select_best_candidate(self) -> None:
        evolver = PromptEvolver()
        candidates = ("a", "b", "c")
        scores = (0.3, 0.9, 0.5)
        assert evolver.select(candidates, scores) == "b"

    def test_select_empty_returns_empty(self) -> None:
        evolver = PromptEvolver()
        assert evolver.select((), ()) == ""
