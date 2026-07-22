from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from core.ids import WorkspaceId
from core.interfaces.workspace_manager import WorkspaceManager
from core.models.workspace import Workspace


@dataclass(slots=True, frozen=True)
class LocalWorkspaceManager(WorkspaceManager):
    """Manages workspaces as local filesystem directories."""

    _workspaces: dict[str, Workspace] = field(default_factory=dict, init=False, repr=False)

    def create(self, name: str, root_path: str) -> Workspace:
        """Create a new workspace directory and register it.

        Args:
            name: Human-readable workspace name.
            root_path: Filesystem path for the workspace root.

        Returns:
            A new workspace with active=True.
        """
        path = Path(root_path)
        path.mkdir(parents=True, exist_ok=True)
        ws = Workspace(id=WorkspaceId(f"ws-{name}"), name=name, root_path=str(path.resolve()))
        self._workspaces[ws.id] = ws
        return ws

    def get(self, workspace_id: str) -> Workspace | None:
        """Retrieve a workspace by its identifier.

        Args:
            workspace_id: The unique identifier of the workspace.

        Returns:
            The workspace if found, None otherwise.
        """
        return self._workspaces.get(workspace_id)

    def list_active(self) -> tuple[Workspace, ...]:
        """Retrieve all active workspaces.

        Returns:
            An immutable tuple of active workspaces.
        """
        return tuple(ws for ws in self._workspaces.values() if ws.active)

    def destroy(self, workspace_id: str) -> None:
        """Mark a workspace as inactive and remove its directory.

        Args:
            workspace_id: The identifier of the workspace to destroy.

        Raises:
            KeyError: If no workspace exists with the given id.
        """
        ws = self._workspaces.get(workspace_id)
        if ws is None:
            raise KeyError(workspace_id)
        path = Path(ws.root_path)
        if path.exists():
            shutil.rmtree(path)
        del self._workspaces[workspace_id]
