"""Windsurf IDE adapter (.windsurf/rules/<id>.md)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from adapters.base import BaseAdapter, sha256_file
from adapters.cursor import strip_frontmatter


class WindsurfAdapter(BaseAdapter):
    """Adapter for Windsurf IDE (.windsurf/rules/<id>.md)."""

    name = "windsurf"
    aliases = ("windsurf", "codeium")
    description = "Windsurf Cascade rules (.windsurf/rules/<id>.md)"
    discovery_path = ".windsurf/rules/{id}.md"

    def get_destination_path(self, project_dir: Path, skill_id: str) -> Path:
        return project_dir / ".windsurf" / "rules" / f"{skill_id}.md"

    def install(
        self,
        project_dir: Path,
        resource: dict[str, Any],
        source_dir: Path,
        mode: str = "copy",
    ) -> tuple[Path, dict[str, Any]]:
        dest = self.get_destination_path(project_dir, resource["id"])
        dest.parent.mkdir(parents=True, exist_ok=True)

        skill_md = source_dir / "SKILL.md"
        if not skill_md.is_file():
            raise FileNotFoundError(f"{skill_md} does not exist")

        text = skill_md.read_text(encoding="utf-8")
        fields, body = strip_frontmatter(text)

        desc = fields.get("description", resource.get("description", resource["id"]))
        content = (
            f"# Rule: {resource['id']}\n\n"
            f"> **Purpose**: {desc}\n\n"
            f"{body}\n"
        )
        dest.write_text(content, encoding="utf-8")
        sha = sha256_file(dest)

        record = {
            "agent": self.name,
            "mode": "copy",
            "source": str(source_dir.resolve()),
            "destination": str(dest.relative_to(project_dir)),
            "sha256": sha,
            "treeSha256": sha,
        }
        return dest, record

    def uninstall(
        self,
        project_dir: Path,
        skill_id: str,
        record: dict[str, Any],
    ) -> tuple[bool, str]:
        dest = project_dir / record.get("destination", f".windsurf/rules/{skill_id}.md")
        if not os.path.lexists(dest):
            return True, "already absent"

        if not dest.is_file():
            return False, "destination is not a regular file"

        current_sha = sha256_file(dest)
        if record.get("sha256") and current_sha != record["sha256"]:
            return False, "rule file was modified since installation; kept"

        dest.unlink()
        return True, "removed rule file"

    def verify(
        self,
        project_dir: Path,
        skill_id: str,
        record: dict[str, Any],
    ) -> tuple[bool, str]:
        dest = project_dir / record.get("destination", f".windsurf/rules/{skill_id}.md")
        if not dest.is_file():
            return False, "rule file missing from disk"
        if record.get("sha256") and sha256_file(dest) != record["sha256"]:
            return False, "rule content modified"
        return True, "valid"
