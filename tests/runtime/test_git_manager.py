from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import pytest

from runtime.git_manager import LocalGitManager


# ---------------------------------------------------------------------------
# Interface compliance
# ---------------------------------------------------------------------------


def test_interface_is_abstract() -> None:
    from core.interfaces.git_manager import GitManager

    with pytest.raises(TypeError):
        GitManager()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# init()
# ---------------------------------------------------------------------------


def test_init_creates_git_directory() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        target = str(Path(tmpdir) / "repo")
        ws = mgr.init(target)
        assert (Path(target) / ".git").is_dir()


def test_init_returns_workspace_with_correct_name() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.init(str(Path(tmpdir) / "my-repo"))
        assert ws.name == "my-repo"


def test_init_returns_resolved_root_path() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        target = str(Path(tmpdir) / "repo")
        ws = mgr.init(target)
        assert ws.root_path == str(Path(target).resolve())


def test_init_creates_parent_directories() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        nested = str(Path(tmpdir) / "a" / "b" / "repo")
        ws = mgr.init(nested)
        assert (Path(nested) / ".git").is_dir()
        assert ws.name == "repo"


def test_init_bare_creates_bare_repo() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        target = str(Path(tmpdir) / "bare-repo")
        ws = mgr.init(target, bare=True)
        # bare repos have HEAD, objects, refs directly — no .git subdir
        assert (Path(target) / "HEAD").exists()
        assert (Path(target) / "objects").is_dir()
        assert (Path(target) / "refs").is_dir()


def test_init_raises_if_git_dir_exists() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        target = str(Path(tmpdir) / "repo")
        mgr.init(target)
        with pytest.raises(FileExistsError):
            mgr.init(target)


# ---------------------------------------------------------------------------
# initialize_if_needed()
# ---------------------------------------------------------------------------


def test_initialize_if_needed_creates_git_directory() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        target = str(Path(tmpdir) / "repo")
        mgr.initialize_if_needed(target)
        assert (Path(target) / ".git").is_dir()


def test_initialize_if_needed_succeeds_when_git_exists() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        target = str(Path(tmpdir) / "repo")
        mgr.init(target)
        mgr.initialize_if_needed(target)
        assert (Path(target) / ".git").is_dir()


def test_initialize_if_needed_creates_parent_directories() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        nested = str(Path(tmpdir) / "a" / "b" / "repo")
        mgr.initialize_if_needed(nested)
        assert (Path(nested) / ".git").is_dir()


# ---------------------------------------------------------------------------
# branch()
# ---------------------------------------------------------------------------


def _make_repo(mgr: LocalGitManager, tmpdir: str, name: str = "repo") -> str:
    """Helper: init a repo and make an initial commit (branches need one)."""
    ws = mgr.init(str(Path(tmpdir) / name))
    # Create a file so git branch works (git needs at least one commit)
    (Path(ws.root_path) / "init.txt").write_text("x")
    mgr.commit(ws, "initial")
    return ws.root_path


def test_branch_returns_name() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        result = mgr.branch(ws, "feature-a")
        assert result == "feature-a"


def test_branch_creates_branch_in_repo() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        mgr.branch(ws, "dev")
        # Verify branch exists via git
        result = subprocess.run(
            ["git", "branch", "--list", "dev"],
            cwd=ws_path,
            capture_output=True,
            text=True,
        )
        assert "dev" in result.stdout


def test_branch_raises_value_error_for_duplicate() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        mgr.branch(ws, "feature")
        with pytest.raises(ValueError):
            mgr.branch(ws, "feature")


# ---------------------------------------------------------------------------
# commit()
# ---------------------------------------------------------------------------


def test_commit_returns_hash() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        (Path(ws_path) / "file.txt").write_text("hello")
        commit_hash = mgr.commit(ws, "add file")
        assert len(commit_hash) == 40  # full SHA-1
        assert all(c in "0123456789abcdef" for c in commit_hash)


def test_commit_stages_all_changes() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        (Path(ws_path) / "a.txt").write_text("aaa")
        (Path(ws_path) / "b.txt").write_text("bbb")
        mgr.commit(ws, "two files")
        # status should be clean after commit
        status = mgr.status(ws)
        assert status.strip() == ""


def test_commit_empty_repo_fails() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        # No changes to commit — git commit will fail
        with pytest.raises(subprocess.CalledProcessError):
            mgr.commit(ws, "nothing to commit")


# ---------------------------------------------------------------------------
# diff()
# ---------------------------------------------------------------------------


def test_diff_returns_empty_when_clean() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        assert mgr.diff(ws) == ""


def test_diff_shows_unstaged_changes() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        # Modify a tracked file — git diff shows tracked-file changes only
        (Path(ws_path) / "init.txt").write_text("modified content")
        diff = mgr.diff(ws)
        assert "init.txt" in diff
        assert "modified content" in diff


# ---------------------------------------------------------------------------
# status()
# ---------------------------------------------------------------------------


def test_status_returns_empty_when_clean() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        assert mgr.status(ws).strip() == ""


def test_status_shows_untracked_files() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        (Path(ws_path) / "untracked.txt").write_text("??")
        status = mgr.status(ws)
        assert "untracked.txt" in status


def test_status_shows_modified_files() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        (Path(ws_path) / "init.txt").write_text("modified")
        status = mgr.status(ws)
        assert "M" in status


# ---------------------------------------------------------------------------
# push()
# ---------------------------------------------------------------------------


def test_push_raises_when_no_remote() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws_path = _make_repo(mgr, tmpdir)
        from core.models.workspace import Workspace
        from core.ids import WorkspaceId

        ws = Workspace(id=WorkspaceId("ws-test"), name="repo", root_path=ws_path)
        with pytest.raises(RuntimeError):
            mgr.push(ws)


def test_push_to_local_remote() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        remote_path = str(Path(tmpdir) / "remote.git")
        mgr.init(remote_path, bare=True)

        clone_path = str(Path(tmpdir) / "work")
        ws = mgr.clone(f"file://{remote_path}", clone_path)

        (Path(clone_path) / "file.txt").write_text("hello")
        mgr.commit(ws, "initial commit")

        output = mgr.push(ws, remote="origin", branch="master")
        assert isinstance(output, str)


# ---------------------------------------------------------------------------
# Integration: init → commit → branch → diff → status
# ---------------------------------------------------------------------------


def test_full_lifecycle() -> None:
    mgr = LocalGitManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = mgr.init(str(Path(tmpdir) / "lifecycle"))
        # Commit initial content
        (Path(ws.root_path) / "a.txt").write_text("a")
        h1 = mgr.commit(ws, "first")
        assert len(h1) == 40

        # Create branch
        mgr.branch(ws, "feature")
        (Path(ws.root_path) / "a.txt").write_text("updated")
        diff = mgr.diff(ws)
        assert "a.txt" in diff

        status = mgr.status(ws)
        assert "a.txt" in status
