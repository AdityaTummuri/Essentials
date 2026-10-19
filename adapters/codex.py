"""OpenAI Codex and Agent Skills standard adapter."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from adapters.base import BaseAdapter, sha256_file, tree_digest


class CodexAdapter(BaseAdapter):
    """Adapter for OpenAI Codex & Agent Skills standard (.agents/skills/<id>/)."""

    name = "codex"
    aliases = ("codex", "openai", "agent-skills")
    description = "OpenAI Codex and standard agent skills (.agents/skills/<id>/)"
    discovery_path = ".agents/skills/{id}/SKILL.md"

    def get_destination_path(self, project_dir: Path, skill_id: str) -> Path:
        return project_dir / ".agents" / "skills" / skill_id

    def install(
        self,
        project_dir: Path,
        resource: dict[str, Any],
        source_dir: Path,
        mode: str = "link",
    ) -> tuple[Path, dict[str, Any]]:
        dest = self.get_destination_path(project_dir, resource["id"])
        dest.parent.mkdir(parents=True, exist_ok=True)

        skill_md = source_dir / "SKILL.md"
        sha = sha256_file(skill_md) if skill_md.is_file() else ""
        tree_sha = tree_digest(source_dir) if source_dir.is_dir() else ""

        if mode == "link":
            os.symlink(source_dir.resolve(), dest, target_is_directory=True)
        else:
            shutil.copytree(source_dir.resolve(), dest, symlinks=False)

        record = {
            "agent": self.name,
            "mode": mode,
            "source": str(source_dir.resolve()),
            "destination": str(dest.relative_to(project_dir)),
            "sha256": sha,
            "treeSha256": tree_sha,
        }
        return dest, record

    def uninstall(
        self,
        project_dir: Path,
        skill_id: str,
        record: dict[str, Any],
    ) -> tuple[bool, str]:
        dest = project_dir / record.get("destination", f".agents/skills/{skill_id}")
        if not os.path.lexists(dest):
            return True, "already absent"

        if record.get("mode") == "link":
            if dest.is_symlink():
                expected = record.get("source")
                if expected and os.readlink(dest) != expected:
                    return False, f"symlink was altered to point to {os.readlink(dest)}"
                dest.unlink()
                return True, "unlinked"
            return False, "expected symlink but found directory"
        else:
            if dest.is_dir() and not dest.is_symlink():
                current_tree = tree_digest(dest)
                if record.get("treeSha256") and current_tree != record["treeSha256"]:
                    return False, "directory was modified since installation; kept"
                shutil.rmtree(dest)
                return True, "removed copy"
            return False, "destination is not a directory"

    def verify(
        self,
        project_dir: Path,
        skill_id: str,
        record: dict[str, Any],
    ) -> tuple[bool, str]:
        dest = project_dir / record.get("destination", f".agents/skills/{skill_id}")
        if not os.path.lexists(dest):
            return False, "missing from disk"
        skill_md = dest / "SKILL.md"
        if not skill_md.is_file():
            return False, "SKILL.md missing"
        if record.get("mode") == "link":
            if not dest.is_symlink():
                return False, "expected symlink"
            if record.get("source") and os.readlink(dest) != record["source"]:
                return False, "symlink destination changed"
        elif record.get("sha256") and sha256_file(skill_md) != record["sha256"]:
            return False, "SKILL.md content changed"
        return True, "valid"
