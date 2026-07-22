from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from core.ids import WorkspaceId
from core.interfaces.git_manager import GitManager
from core.models.workspace import Workspace


@dataclass(slots=True, frozen=True)
class LocalGitManager(GitManager):
    """Performs git operations using the local git CLI."""

    def init(self, path: str, bare: bool = False) -> Workspace:
        """Initialize a new git repository at the given path.

        Args:
            path: The directory in which to create the repository.
            bare: When True, create a bare repository.

        Returns:
            A workspace rooted at the initialized repository.

        Raises:
            FileExistsError: If ``path/.git`` already exists.
            RuntimeError: If the git command fails.
        """
        repo_path = Path(path)
        git_dir = repo_path / ".git" if not bare else repo_path
        if git_dir.exists():
            raise FileExistsError(str(git_dir))
        repo_path.mkdir(parents=True, exist_ok=True)
        cmd = ["git", "init"]
        if bare:
            cmd.append("--bare")
        cmd.append(path)
        subprocess.run(cmd, check=True, capture_output=True)
        name = repo_path.name
        return Workspace(
            id=WorkspaceId(f"ws-git-{name}"),
            name=name,
            root_path=str(repo_path.resolve()),
        )

    def branch(self, workspace: Workspace, name: str) -> str:
        """Create a new branch in the workspace repository.

        Args:
            workspace: The workspace containing the repository.
            name: The branch name to create.

        Returns:
            The created branch name.

        Raises:
            ValueError: If the branch already exists.
            RuntimeError: If the git command fails.
        """
        result = subprocess.run(
            ["git", "branch", name],
            cwd=workspace.root_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            if "already exists" in stderr:
                raise ValueError(name)
            raise RuntimeError(stderr or f"git branch failed with code {result.returncode}")
        return name

    def initialize_if_needed(self, path: str) -> None:
        """Initialize a git repository if one does not already exist.

        This is a safe alternative to ``init()`` that silently succeeds
        when ``.git`` is already present.

        Args:
            path: The directory in which to initialize the repository.
        """
        repo_path = Path(path)
        git_dir = repo_path / ".git"
        if git_dir.exists():
            return
        repo_path.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "init", path],
            check=True,
            capture_output=True,
        )

    def clone(self, url: str, target_path: str) -> Workspace:
        """Clone a remote repository into a local path.

        Args:
            url: The remote repository URL.
            target_path: The local directory to clone into.

        Returns:
            A workspace rooted at the cloned repository.
        """
        subprocess.run(
            ["git", "clone", url, target_path],
            check=True,
            capture_output=True,
        )
        name = target_path.split("/")[-1]
        return Workspace(
            id=WorkspaceId(f"ws-git-{target_path}"),
            name=name,
            root_path=target_path,
        )

    def commit(self, workspace: Workspace, message: str) -> str:
        """Stage all changes and create a commit.

        Args:
            workspace: The workspace containing the repository.
            message: The commit message.

        Returns:
            The created commit hash.
        """
        subprocess.run(
            ["git", "add", "-A"],
            cwd=workspace.root_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=workspace.root_path,
            capture_output=True,
            text=True,
            check=True,
        )
        log = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace.root_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return log.stdout.strip()

    def diff(self, workspace: Workspace) -> str:
        """Get the unstaged diff for the workspace.

        Args:
            workspace: The workspace to diff.

        Returns:
            A unified diff string of all changes.
        """
        result = subprocess.run(
            ["git", "diff"],
            cwd=workspace.root_path,
            capture_output=True,
            text=True,
        )
        return result.stdout

    def status(self, workspace: Workspace) -> str:
        """Get the current git status.

        Args:
            workspace: The workspace to check.

        Returns:
            The git status output string.
        """
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=workspace.root_path,
            capture_output=True,
            text=True,
        )
        return result.stdout

    def push(self, workspace: Workspace, remote: str = "origin", branch: str | None = None) -> str:
        """Push commits to a remote repository.

        Args:
            workspace: The workspace containing the repository.
            remote: The remote name to push to (default: "origin").
            branch: The branch to push (default: current branch).

        Returns:
            The git push output string.

        Raises:
            RuntimeError: If the git command fails.
        """
        cmd = ["git", "push", remote]
        if branch:
            cmd.append(branch)
        result = subprocess.run(
            cmd,
            cwd=workspace.root_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            raise RuntimeError(stderr or f"git push failed with code {result.returncode}")
        return result.stdout + result.stderr
