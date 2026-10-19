"""GitHub Copilot adapter (.github/prompts/<id>.prompt.md)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from adapters.base import BaseAdapter, sha256_file
from adapters.cursor import strip_frontmatter


class CopilotAdapter(BaseAdapter):
    """Adapter for GitHub Copilot (.github/prompts/<id>.prompt.md)."""

    name = "copilot"
    aliases = ("copilot", "github-copilot")
    description = "GitHub Copilot prompt instructions (.github/prompts/<id>.prompt.md)"
    discovery_path = ".github/prompts/{id}.prompt.md"

    def get_destination_path(self, project_dir: Path, skill_id: str) -> Path:
        return project_dir / ".github" / "prompts" / f"{skill_id}.prompt.md"

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
            f"# Copilot Prompt: {resource['id']}\n\n"
            f"> {desc}\n\n"
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
        dest = project_dir / record.get("destination", f".github/prompts/{skill_id}.prompt.md")
        if not os.path.lexists(dest):
            return True, "already absent"

        if not dest.is_file():
            return False, "destination is not a regular file"

        current_sha = sha256_file(dest)
        if record.get("sha256") and current_sha != record["sha256"]:
            return False, "prompt file was modified since installation; kept"

        dest.unlink()
        return True, "removed prompt file"

    def verify(
        self,
        project_dir: Path,
        skill_id: str,
        record: dict[str, Any],
    ) -> tuple[bool, str]:
        dest = project_dir / record.get("destination", f".github/prompts/{skill_id}.prompt.md")
        if not dest.is_file():
            return False, "prompt file missing from disk"
        if record.get("sha256") and sha256_file(dest) != record["sha256"]:
            return False, "prompt content modified"
        return True, "valid"

