"""Base adapter interface for multi-agent skill installations."""

from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path
from typing import Tuple, Dict, Any


def sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> str:
    """Hash every file's relative path and contents in sorted order."""
    digest = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames):
            full = Path(dirpath) / name
            digest.update(str(full.relative_to(root)).encode())
            digest.update(sha256_file(full).encode())
    return digest.hexdigest()


class BaseAdapter:
    """Base adapter class for adapting canonical skills to specific agents."""

    name: str = "base"
    aliases: tuple[str, ...] = ()
    description: str = "Base agent adapter"
    discovery_path: str = ""

    def get_destination_path(self, project_dir: Path, skill_id: str) -> Path:
        """Return the target path for this skill in the project."""
        raise NotImplementedError

    def install(
        self,
        project_dir: Path,
        resource: dict[str, Any],
        source_dir: Path,
        mode: str = "link",
    ) -> tuple[Path, dict[str, Any]]:
        """Install the resource into the project for this agent."""
        raise NotImplementedError

    def uninstall(
        self,
        project_dir: Path,
        skill_id: str,
        record: dict[str, Any],
    ) -> tuple[bool, str]:
        """Safely remove the installed resource if it was not modified."""
        raise NotImplementedError

    def verify(
        self,
        project_dir: Path,
        skill_id: str,
        record: dict[str, Any],
    ) -> tuple[bool, str]:
        """Verify the integrity of an existing installation."""
        raise NotImplementedError

