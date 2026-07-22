from core.interfaces.planner import Planner


def test_planner_is_abstract() -> None:
    try:
        Planner()
        assert False, "Should not be instantiable"
    except TypeError:
        pass
