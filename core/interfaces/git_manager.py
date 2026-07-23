from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.workspace import Workspace


@runtime_checkable
class GitManager(Protocol):
    """Performs git operations within workspace contexts."""

    def init(self, path: str, bare: bool = False) -> Workspace:
        """Initialize a new git repository.

        Args:
            path: The directory in which to create the repository.
            bare: When True, create a bare repository.

        Returns:
            A workspace rooted at the initialized repository.

        Raises:
            FileExistsError: If ``path/.git`` already exists.
            RuntimeError: If the git command fails.
        """

    def initialize_if_needed(self, path: str) -> None:
        """Initialize a git repository if one does not already exist.

        This is a safe alternative to ``init()`` that silently succeeds
        when ``.git`` is already present.

        Args:
            path: The directory in which to initialize the repository.
        """

    def clone(self, url: str, target_path: str) -> Workspace:
        """Clone a remote repository into a local path.

        Args:
            url: The remote repository URL.
            target_path: The local directory to clone into.

        Returns:
            A workspace rooted at the cloned repository.
        """

    def branch(self, workspace: Workspace, name: str) -> str:
        """Create a new branch and return its name.

        Args:
            workspace: The workspace containing the repository.
            name: The branch name to create.

        Returns:
            The created branch name.

        Raises:
            ValueError: If the branch already exists.
            RuntimeError: If the git command fails.
        """

    def commit(self, workspace: Workspace, message: str) -> str:
        """Stage all changes and create a commit.

        Args:
            workspace: The workspace containing the repository.
            message: The commit message.

        Returns:
            The created commit hash.
        """

    def diff(self, workspace: Workspace) -> str:
        """Get the unstaged diff for the workspace.

        Args:
            workspace: The workspace to diff.

        Returns:
            A unified diff string of all changes.
        """

    def status(self, workspace: Workspace) -> str:
        """Get the current git status.

        Args:
            workspace: The workspace to check.

        Returns:
            The git status output string.
        """

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
