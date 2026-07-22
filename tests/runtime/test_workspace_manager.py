from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pytest

from core.ids import WorkspaceId
from runtime.workspace_manager import LocalWorkspaceManager


# ---------------------------------------------------------------------------
# Interface compliance
# ---------------------------------------------------------------------------


def test_interface_is_abstract() -> None:
    from core.interfaces.workspace_manager import WorkspaceManager

    with pytest.raises(TypeError):
        WorkspaceManager()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# create()
# ---------------------------------------------------------------------------


def test_create_returns_workspace_with_correct_name() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("my-project", tmpdir)
        assert ws.name == "my-project"


def test_create_returns_active_workspace() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("proj", tmpdir)
        assert ws.active is True


def test_create_uses_prefixed_id() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("alpha", tmpdir)
        assert ws.id == WorkspaceId("ws-alpha")


def test_create_resolves_root_path() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("proj", tmpdir)
        assert ws.root_path == str(Path(tmpdir).resolve())


def test_create_makes_directory() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        target = str(Path(tmpdir) / "new-ws")
        mgr.create("proj", target)
        assert Path(target).is_dir()


def test_create_makes_parent_directories() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        nested = str(Path(tmpdir) / "a" / "b" / "c")
        mgr.create("deep", nested)
        assert Path(nested).is_dir()


def test_create_existing_directory_does_not_raise() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws1 = mgr.create("proj", tmpdir)
        ws2 = mgr.create("proj", tmpdir)
        assert ws1.id == ws2.id


# ---------------------------------------------------------------------------
# get()
# ---------------------------------------------------------------------------


def test_get_returns_workspace_by_id() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        created = mgr.create("proj", tmpdir)
        found = mgr.get(created.id)
        assert found is created


def test_get_returns_none_for_missing_id() -> None:
    mgr = LocalWorkspaceManager()
    assert mgr.get("ws-nonexistent") is None


def test_get_returns_none_for_empty_string() -> None:
    mgr = LocalWorkspaceManager()
    assert mgr.get("") is None


# ---------------------------------------------------------------------------
# list_active()
# ---------------------------------------------------------------------------


def test_list_active_empty_when_no_workspaces() -> None:
    mgr = LocalWorkspaceManager()
    assert mgr.list_active() == ()


def test_list_active_returns_tuple() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr.create("proj", tmpdir)
        result = mgr.list_active()
        assert isinstance(result, tuple)


def test_list_active_returns_created_workspaces() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("proj", tmpdir)
        active = mgr.list_active()
        assert len(active) == 1
        assert active[0] is ws


def test_list_active_multiple_workspaces() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory() as tmpdir2:
        ws1 = mgr.create("alpha", tmpdir1)
        ws2 = mgr.create("beta", tmpdir2)
        active = mgr.list_active()
        assert len(active) == 2
        ids = {ws.id for ws in active}
        assert ws1.id in ids
        assert ws2.id in ids


def test_list_active_excludes_destroyed() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory() as tmpdir2:
        ws_keep = mgr.create("keep", tmpdir1)
        ws_remove = mgr.create("remove", tmpdir2)
        mgr.destroy(ws_remove.id)
        active = mgr.list_active()
        assert len(active) == 1
        assert active[0] is ws_keep


# ---------------------------------------------------------------------------
# destroy()
# ---------------------------------------------------------------------------


def test_destroy_removes_workspace() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("proj", tmpdir)
        mgr.destroy(ws.id)
        assert mgr.get(ws.id) is None


def test_destroy_removes_directory() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("proj", tmpdir)
        assert Path(tmpdir).is_dir()
        mgr.destroy(ws.id)
        assert not Path(tmpdir).exists()


def test_destroy_raises_key_error_for_missing() -> None:
    mgr = LocalWorkspaceManager()
    with pytest.raises(KeyError):
        mgr.destroy("ws-nonexistent")


def test_destroy_does_not_affect_other_workspaces() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory() as tmpdir2:
        ws1 = mgr.create("alpha", tmpdir1)
        ws2 = mgr.create("beta", tmpdir2)
        mgr.destroy(ws1.id)
        assert mgr.get(ws2.id) is ws2
        assert len(mgr.list_active()) == 1


def test_destroy_nonexistent_directory_is_idempotent() -> None:
    """Destroying a workspace whose directory was already removed."""
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("proj", tmpdir)
        shutil.rmtree(tmpdir)
        mgr.destroy(ws.id)
        assert mgr.get(ws.id) is None


# ---------------------------------------------------------------------------
# Integration: create → get → destroy lifecycle
# ---------------------------------------------------------------------------


def test_full_lifecycle() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.create("lifecycle", tmpdir)
        assert ws.active is True
        assert mgr.get(ws.id) is ws
        assert len(mgr.list_active()) == 1

        mgr.destroy(ws.id)
        assert mgr.get(ws.id) is None
        assert len(mgr.list_active()) == 0
        assert not Path(tmpdir).exists()


def test_multiple_workspaces_lifecycle() -> None:
    mgr = LocalWorkspaceManager()
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        ws_a = mgr.create("a", d1)
        ws_b = mgr.create("b", d2)
        assert len(mgr.list_active()) == 2

        mgr.destroy(ws_a.id)
        assert len(mgr.list_active()) == 1
        assert mgr.get(ws_b.id) is ws_b

        mgr.destroy(ws_b.id)
        assert len(mgr.list_active()) == 0
