from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from core.ids import WorkspaceId
from core.interfaces.execution_engine import ExecutionEngine
from core.models.execution import ExecutionStatus
from core.models.workspace import Workspace
from src.opencode.adapter import OpenCodeAdapter


def _make_workspace(tmpdir: str) -> Workspace:
    return Workspace(
        id=WorkspaceId("ws-test"),
        name="test-workspace",
        root_path=tmpdir,
    )


class TestOpenCodeAdapterInterface:
    def test_implements_execution_engine(self) -> None:
        adapter = OpenCodeAdapter()
        assert isinstance(adapter, ExecutionEngine)

    def test_cannot_instantiate_abc(self) -> None:
        with pytest.raises(TypeError):
            ExecutionEngine()  # type: ignore[abstract]


class TestOpenCodeAdapterRun:
    def test_run_returns_execution(self) -> None:
        adapter = OpenCodeAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            mock_result = subprocess.CompletedProcess(
                args=["opencode", "run", "hello"],
                returncode=0,
                stdout="output text",
                stderr="",
            )
            with patch("subprocess.run", return_value=mock_result):
                result = adapter.run("hello", ws)
            assert result.status == ExecutionStatus.COMPLETED
            assert "output text" in result.outputs

    def test_run_captures_stdout(self) -> None:
        adapter = OpenCodeAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            mock_result = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="stdout data", stderr="",
            )
            with patch("subprocess.run", return_value=mock_result):
                result = adapter.run("test", ws)
            output = adapter.get_output(result.id.replace("exec-", ""))
            assert output == "stdout data"

    def test_run_failed_returns_failed_status(self) -> None:
        adapter = OpenCodeAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            mock_result = subprocess.CompletedProcess(
                args=[], returncode=1, stdout="", stderr="error msg",
            )
            with patch("subprocess.run", return_value=mock_result):
                result = adapter.run("fail", ws)
            assert result.status == ExecutionStatus.FAILED
            assert result.error == "error msg"

    def test_run_timeout_returns_timed_out(self) -> None:
        adapter = OpenCodeAdapter(timeout_seconds=0.001)
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="opencode", timeout=0.001)):
                result = adapter.run("slow", ws)
            assert result.status == ExecutionStatus.TIMED_OUT
            assert result.error == "Execution timed out"

    def test_run_missing_binary_returns_failed(self) -> None:
        adapter = OpenCodeAdapter(opencode_bin="/nonexistent/opencode")
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            result = adapter.run("test", ws)
            assert result.status == ExecutionStatus.FAILED
            assert "not found" in result.error

    def test_run_passes_code_as_message(self) -> None:
        adapter = OpenCodeAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            mock_result = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="ok", stderr="",
            )
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                adapter.run("write a function", ws)
            call_args = mock_run.call_args
            assert "write a function" in call_args[0][0]

    def test_run_uses_workspace_root_as_cwd(self) -> None:
        adapter = OpenCodeAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            mock_result = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="", stderr="",
            )
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                adapter.run("test", ws)
            assert mock_run.call_args[1]["cwd"] == tmpdir


class TestOpenCodeAdapterGetOutputError:
    def test_get_output_returns_captured_stdout(self) -> None:
        adapter = OpenCodeAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            mock_result = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="hello world", stderr="",
            )
            with patch("subprocess.run", return_value=mock_result):
                result = adapter.run("test", ws)
            output = adapter.get_output(result.id.replace("exec-", ""))
            assert output == "hello world"

    def test_get_error_returns_none_when_no_error(self) -> None:
        adapter = OpenCodeAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            mock_result = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="ok", stderr="",
            )
            with patch("subprocess.run", return_value=mock_result):
                result = adapter.run("test", ws)
            assert adapter.get_error("nonexistent") is None

    def test_get_error_returns_stderr(self) -> None:
        adapter = OpenCodeAdapter()
        with tempfile.TemporaryDirectory() as tmpdir:
            ws = _make_workspace(tmpdir)
            mock_result = subprocess.CompletedProcess(
                args=[], returncode=1, stdout="", stderr="fatal error",
            )
            with patch("subprocess.run", return_value=mock_result):
                result = adapter.run("fail", ws)
            error = adapter.get_error(result.id.replace("exec-", ""))
            assert error == "fatal error"
