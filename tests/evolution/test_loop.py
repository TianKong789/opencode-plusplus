from evolution.loop import EvolutionLoop


def test_evolution_loop_iteration() -> None:
    loop = EvolutionLoop(max_iterations=3)
    assert loop.should_continue() is True

    loop2 = loop.record_iteration()
    assert loop2.current_iteration == 1

    loop3 = loop2.record_iteration().record_iteration()
    assert loop3.should_continue() is False
