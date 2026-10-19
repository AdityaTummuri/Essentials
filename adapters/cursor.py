"""Cursor IDE adapter (.cursor/rules/<id>.mdc)."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from adapters.base import BaseAdapter, sha256_file


def strip_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Extract YAML frontmatter and remaining markdown body."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, val = line.split(":", 1)
            fields[key.strip()] = val.strip().strip('"\'')
    return fields, match.group(2).strip()


class CursorAdapter(BaseAdapter):
    """Adapter for Cursor IDE Rules (.cursor/rules/<id>.mdc)."""

    name = "cursor"
    aliases = ("cursor", "cursor-ide", "cursorrules")
    description = "Cursor MDC project rules (.cursor/rules/<id>.mdc)"
    discovery_path = ".cursor/rules/{id}.mdc"

    def get_destination_path(self, project_dir: Path, skill_id: str) -> Path:
        return project_dir / ".cursor" / "rules" / f"{skill_id}.mdc"

    def install(
        self,
        project_dir: Path,
        resource: dict[str, Any],
        source_dir: Path,
        mode: str = "copy",
    ) -> tuple[Path, dict[str, Any]]:
        # Cursor rules are always generated files (mode is copy)
        dest = self.get_destination_path(project_dir, resource["id"])
        dest.parent.mkdir(parents=True, exist_ok=True)

        skill_md = source_dir / "SKILL.md"
        if not skill_md.is_file():
            raise FileNotFoundError(f"{skill_md} does not exist")

        text = skill_md.read_text(encoding="utf-8")
        fields, body = strip_frontmatter(text)

        desc = fields.get("description", resource.get("description", resource["id"]))
        # Format Cursor MDC
        mdc_content = (
            f"---\n"
            f"description: {desc}\n"
            f"globs: *\n"
            f"alwaysApply: false\n"
            f"---\n\n"
            f"# {resource['id']}\n\n"
            f"{body}\n"
        )
        dest.write_text(mdc_content, encoding="utf-8")
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
        dest = project_dir / record.get("destination", f".cursor/rules/{skill_id}.mdc")
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
        dest = project_dir / record.get("destination", f".cursor/rules/{skill_id}.mdc")
        if not dest.is_file():
            return False, "rule file missing from disk"
        if record.get("sha256") and sha256_file(dest) != record["sha256"]:
            return False, "rule content modified"
        return True, "valid"

