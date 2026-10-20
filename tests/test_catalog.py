"""Provenance and integrity checks for resources/resources.json.

Verifies:
- Every categorised skill with a SKILL.md has a catalog entry
- Catalog ids are unique
- Vendored catalog entries point at an existing skill whose SKILL.md hash matches
- skills/ contains real files and directories only (no symlinks)
- A skill with executable code is never marked safeForDefault unless it has a
  recorded audit below
- skills/ holds no hook, settings, MCP, plugin manifest, or cache artifacts
"""

from __future__ import annotations

import hashlib
import json
import os
import unittest

from scripts.essentials_cli import REPO_ROOT, SKILLS_DIR, scan_skills

CATALOG_PATH = REPO_ROOT / "resources" / "resources.json"

# Suffixes that make a file code. Executable bits on documentation files are ignored.
CODE_SUFFIXES = {".py", ".sh", ".js", ".cjs", ".mjs", ".ts", ".ps1"}
DOC_SUFFIXES = {".md", ".txt", ".html", ".csv", ".json"}

# safeForDefault may be true for a skill with code only after a manual audit.
# Each entry records what was checked (see securityReview.notes in the catalog).
AUDITED_LOCAL_ONLY = {
    "ui-ux-pro-max": "stdlib-only scripts; no network, subprocess, or credentials; writes only with --persist to a chosen directory",
}


def _load_catalog() -> list[dict]:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["resources"]


def _has_code(folder) -> bool:
    for path in folder.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix in CODE_SUFFIXES:
            return True
        if path.suffix not in DOC_SUFFIXES and os.access(path, os.X_OK):
            return True
    return False


class CatalogIntegrityTests(unittest.TestCase):
    """Keeps the provenance catalog in step with the skills on disk."""

    def test_every_categorised_skill_has_catalog_entry(self) -> None:
        catalog_ids = {entry["id"] for entry in _load_catalog()}
        on_disk = {
            skill_id
            for skill_id, meta in scan_skills().items()
            if meta["hasSkillMd"]
        }
        missing = sorted(on_disk - catalog_ids)
        self.assertEqual(missing, [], f"skills without a catalog entry: {missing}")

    def test_catalog_ids_are_unique(self) -> None:
        ids = [entry["id"] for entry in _load_catalog()]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        self.assertEqual(duplicates, [], f"duplicate catalog ids: {duplicates}")

    def test_vendored_skill_hashes_match_skill_md(self) -> None:
        mismatches = []
        for entry in _load_catalog():
            if entry.get("kind") != "skill" or entry.get("status") != "vendored":
                continue
            skill_md = REPO_ROOT / entry["path"] / "SKILL.md"
            if not skill_md.is_file():
                mismatches.append(f"{entry['id']}: SKILL.md missing at {entry['path']}")
                continue
            digest = hashlib.sha256(skill_md.read_bytes()).hexdigest()
            if entry.get("skillMd", {}).get("sha256") != digest:
                mismatches.append(f"{entry['id']}: sha256 differs from catalog")
        self.assertEqual(mismatches, [])

    def test_skills_with_code_are_not_safe_by_default(self) -> None:
        unsafe = []
        for entry in _load_catalog():
            if entry.get("kind") != "skill" or entry.get("status") != "vendored":
                continue
            folder = REPO_ROOT / entry["path"]
            if not folder.is_dir() or not _has_code(folder):
                continue
            if entry.get("safeForDefault") and entry["id"] not in AUDITED_LOCAL_ONLY:
                unsafe.append(entry["id"])
        self.assertEqual(unsafe, [], "skills with code marked safeForDefault without an audit")

    def test_skills_contain_no_forbidden_artifacts(self) -> None:
        # SECURITY.md: no hooks, settings, MCP config, or plugin manifests in the library.
        forbidden_names = {"hooks.json", "settings.json", "settings.local.json", ".mcp.json"}
        forbidden_dirs = {".claude-plugin", "__pycache__"}
        found = []
        for path in SKILLS_DIR.rglob("*"):
            if path.name in forbidden_names or (path.is_dir() and path.name in forbidden_dirs):
                found.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual(sorted(found), [], "forbidden artifacts found under skills/")

    def test_skills_tree_has_no_symlinks(self) -> None:
        links = sorted(
            str(path.relative_to(REPO_ROOT))
            for path in SKILLS_DIR.rglob("*")
            if path.is_symlink()
        )
        self.assertEqual(links, [], "skills/ must hold real copies, not symlinks")


if __name__ == "__main__":
    unittest.main()
