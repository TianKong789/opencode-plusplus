from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.workspace import Workspace


@runtime_checkable
class WorkspaceManager(Protocol):
    """Creates, retrieves, and destroys workspace environments."""

    def create(self, name: str, root_path: str) -> Workspace:
        """Create a new workspace.

        Args:
            name: Human-readable workspace name.
            root_path: Filesystem path for the workspace root.

        Returns:
            A new workspace with active=True.
        """

    def get(self, workspace_id: str) -> Workspace | None:
        """Retrieve a workspace by its identifier.

        Args:
            workspace_id: The unique identifier of the workspace.

        Returns:
            The workspace if found, None otherwise.
        """

    def list_active(self) -> tuple[Workspace, ...]:
        """Retrieve all active workspaces.

        Returns:
            An immutable tuple of active workspaces.
        """

    def destroy(self, workspace_id: str) -> None:
        """Mark a workspace as inactive and release its resources.

        Args:
            workspace_id: The identifier of the workspace to destroy.

        Raises:
            KeyError: If no workspace exists with the given id.
        """
