from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.workspace import Workspace


class GitManager(ABC):
    """Performs git operations within workspace contexts."""

    @abstractmethod
    def clone(self, url: str, target_path: str) -> Workspace:
        """Clone a remote repository into a local path.

        Args:
            url: The remote repository URL.
            target_path: The local directory to clone into.

        Returns:
            A workspace rooted at the cloned repository.
        """

    @abstractmethod
    def commit(self, workspace: Workspace, message: str) -> str:
        """Stage all changes and create a commit.

        Args:
            workspace: The workspace containing the repository.
            message: The commit message.

        Returns:
            The created commit hash.
        """

    @abstractmethod
    def diff(self, workspace: Workspace) -> str:
        """Get the unstaged diff for the workspace.

        Args:
            workspace: The workspace to diff.

        Returns:
            A unified diff string of all changes.
        """

    @abstractmethod
    def status(self, workspace: Workspace) -> str:
        """Get the current git status.

        Args:
            workspace: The workspace to check.

        Returns:
            The git status output string.
        """
