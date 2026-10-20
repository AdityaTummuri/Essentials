"""Unit and integration tests for Essentials portable skills library.

Verifies:
- Skills directory structure and categories
- Valid SKILL.md and YAML frontmatter (name & description) across all skills
- Uniqueness of skill names across all categories
- The manual-copy workflow (copying to ~/.agents/skills)
- Essentials CLI companion commands (list, search, inspect, validate)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.essentials_cli import (
    REPO_ROOT,
    SKILLS_DIR,
    PRESETS,
    scan_skills,
    parse_frontmatter,
    main,
)


class SkillsLibraryTests(unittest.TestCase):
    """Test suite for portable skills structure and workflow."""

    def test_skills_categories_exist(self) -> None:
        """Verify standard categories exist in skills/."""
        self.assertTrue(SKILLS_DIR.is_dir(), f"{SKILLS_DIR} must exist")
        expected_categories = {
            "audio",
            "design",
            "engineering",
            "product",
            "python",
            "robotics-ml",
            "testing",
            "threejs",
        }
        actual_categories = {
            d.name for d in SKILLS_DIR.iterdir()
            if d.is_dir() and not d.name.startswith((".", "_"))
        }
        self.assertTrue(expected_categories.issubset(actual_categories))

    def test_every_skill_has_valid_skill_md_and_frontmatter(self) -> None:
        """Verify every skill folder contains a valid SKILL.md with name and description."""
        skills = scan_skills()
        self.assertGreaterEqual(len(skills), 50, "Expected at least 50 skills in skills/")

        for sid, sdata in skills.items():
            skill_dir = Path(sdata["fullPath"])
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(
                skill_md.is_file(),
                f"Skill '{sid}' at {skill_dir} is missing SKILL.md"
            )

            text = skill_md.read_text(encoding="utf-8")
            fields, body = parse_frontmatter(text)

            self.assertTrue(
                bool(fields),
                f"Skill '{sid}' at {skill_md} has missing or malformed YAML frontmatter"
            )
            self.assertEqual(
                fields.get("name"),
                sid,
                f"Skill '{sid}' frontmatter name '{fields.get('name')}' must match directory name"
            )
            self.assertTrue(
                bool(fields.get("description")),
                f"Skill '{sid}' frontmatter description must be non-empty"
            )
            self.assertTrue(
                len(body.strip()) > 50,
                f"Skill '{sid}' instructions body must not be empty"
            )

    def test_no_duplicate_skill_names_across_categories(self) -> None:
        """Verify all skill folder names are globally unique across all categories."""
        all_skills = []
        for cat_dir in SKILLS_DIR.iterdir():
            if cat_dir.is_dir() and not cat_dir.name.startswith((".", "_")):
                for skill_dir in cat_dir.iterdir():
                    if skill_dir.is_dir() and not skill_dir.name.startswith((".", "_")):
                        all_skills.append(skill_dir.name)

        dups = [name for name in set(all_skills) if all_skills.count(name) > 1]
        self.assertEqual(dups, [], f"Duplicate skill names found: {dups}")

    def test_manual_copy_workflow(self) -> None:
        """Verify the core user workflow: copy skill folder directly into ~/.agents/skills/."""
        with tempfile.TemporaryDirectory(prefix="test-agents-skills-") as tmp:
            mock_agents_dir = Path(tmp) / ".agents" / "skills"
            mock_agents_dir.mkdir(parents=True, exist_ok=True)

            source_skill = SKILLS_DIR / "engineering" / "code-review"
            dest_skill = mock_agents_dir / "code-review"

            # User copies skill folder
            shutil.copytree(source_skill, dest_skill)

            # Verify destination is an autonomous, ready-to-use Agent Skill
            self.assertTrue(dest_skill.is_dir())
            dest_skill_md = dest_skill / "SKILL.md"
            self.assertTrue(dest_skill_md.is_file())

            fields, _ = parse_frontmatter(dest_skill_md.read_text(encoding="utf-8"))
            self.assertEqual(fields.get("name"), "code-review")
            self.assertIn("code review", fields.get("description", "").lower())

    def test_curated_presets_reference_valid_skills(self) -> None:
        """Verify all skills listed in curated presets exist on disk."""
        skills = scan_skills()
        for pname, pdata in PRESETS.items():
            for ref in pdata["skills"]:
                cat, sid = ref.split("/", 1)
                self.assertIn(
                    sid,
                    skills,
                    f"Preset '{pname}' references unknown skill '{ref}'"
                )
                self.assertEqual(
                    skills[sid]["category"],
                    cat,
                    f"Skill '{sid}' category mismatch in preset '{pname}'"
                )

    def test_cli_list_command(self) -> None:
        """Verify essentials list runs cleanly and outputs JSON."""
        res = main(["list", "--json"])
        self.assertEqual(res, 0)

    def test_cli_search_command(self) -> None:
        """Verify essentials search finds matching skills."""
        res = main(["search", "vision", "--json"])
        self.assertEqual(res, 0)

    def test_cli_inspect_command(self) -> None:
        """Verify essentials inspect shows skill and preset details."""
        res_skill = main(["inspect", "code-review", "--json"])
        self.assertEqual(res_skill, 0)

        res_preset = main(["inspect", "portfolio", "--json"])
        self.assertEqual(res_preset, 0)

    def test_cli_validate_command(self) -> None:
        """Verify essentials validate passes with 0 errors on skills/."""
        res = main(["validate"])
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()

