from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from core.models.execution import ExecutionStatus
from runtime.execution_engine import LocalExecutionEngine


# ---------------------------------------------------------------------------
# Interface compliance
# ---------------------------------------------------------------------------


def test_interface_is_abstract() -> None:
    from core.interfaces.execution_engine import ExecutionEngine

    with pytest.raises(TypeError):
        ExecutionEngine()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# run()
# ---------------------------------------------------------------------------


def test_run_writes_hello_txt() -> None:
    engine = LocalExecutionEngine()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = Path(tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="test", root_path=str(ws_path))
        engine.run("ignored", ws)
        assert (ws_path / "hello.txt").exists()


def test_run_hello_txt_content() -> None:
    engine = LocalExecutionEngine()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = Path(tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="test", root_path=str(ws_path))
        engine.run("ignored", ws)
        assert (ws_path / "hello.txt").read_text() == "hello"


def test_run_returns_completed_execution() -> None:
    engine = LocalExecutionEngine()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = Path(tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="test", root_path=str(ws_path))
        result = engine.run("anything", ws)
        assert result.status == ExecutionStatus.COMPLETED


def test_run_execution_has_output() -> None:
    engine = LocalExecutionEngine()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = Path(tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="test", root_path=str(ws_path))
        result = engine.run("code", ws)
        assert result.outputs == ("hello",)


def test_run_ignores_code_parameter() -> None:
    engine = LocalExecutionEngine()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = Path(tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="test", root_path=str(ws_path))
        r1 = engine.run("first", ws)
        (ws_path / "hello.txt").unlink()
        r2 = engine.run("second", ws)
        assert r1.status == r2.status == ExecutionStatus.COMPLETED


# ---------------------------------------------------------------------------
# get_output() / get_error()
# ---------------------------------------------------------------------------


def test_get_output_returns_none() -> None:
    engine = LocalExecutionEngine()
    assert engine.get_output("any-id") is None


def test_get_error_returns_none() -> None:
    engine = LocalExecutionEngine()
    assert engine.get_error("any-id") is None
