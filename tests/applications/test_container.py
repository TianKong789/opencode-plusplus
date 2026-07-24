from __future__ import annotations

from applications.container import Container


class TestContainer:
    def test_container_instantiates_when_wiring_modules_exist(self) -> None:
        # Given/When: the composition root is instantiated.
        container = Container()

        # Then: dependency-injector resolved every configured wiring module.
        assert container.orchestrator is not None
