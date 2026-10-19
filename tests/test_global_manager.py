"""Unit and integration tests for Essentials global skill management.

Tests cover:
- Global setup & dry-run
- Correct discovery paths and YAML frontmatter verification
- All three agent integrations (Claude Code, OpenCode, VS Code Copilot)
- Synchronization after canonical skill changes
- Preservation of existing unmanaged user skills
- Name collisions and broken link recovery
- Safe uninstall
- Corrupted ledger recovery
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.global_manager import (
    GlobalManagerError,
    find_repo_root,
    get_global_ledger_path,
    read_global_ledger,
    write_global_ledger,
    resolve_active_targets,
    setup_global,
    global_status,
    global_sync,
    global_uninstall,
)
from scripts.essentials_cli import load_manifest, build_cli_parser, main


class GlobalManagerTests(unittest.TestCase):
    """Test suite for global skill management across OpenCode, Claude Code, and Copilot."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="essentials-global-test-")
        self.addCleanup(lambda: shutil.rmtree(self.test_dir, ignore_errors=True))

        self.mock_claude = Path(self.test_dir) / ".claude" / "skills"
        self.mock_agents = Path(self.test_dir) / ".agents" / "skills"
        self.mock_opencode = Path(self.test_dir) / ".config" / "opencode" / "skills"
        self.mock_copilot = Path(self.test_dir) / ".copilot" / "skills"
        self.mock_ledger = Path(self.test_dir) / "config" / "essentials" / "global-ledger.json"

        # Configure environment variables to redirect global targets to test sandbox
        self.env_patch = {
            "CLAUDE_SKILLS_DIR": str(self.mock_claude),
            "AGENTS_SKILLS_DIR": str(self.mock_agents),
            "OPENCODE_SKILLS_DIR": str(self.mock_opencode),
            "COPILOT_SKILLS_DIR": str(self.mock_copilot),
            "ESSENTIALS_GLOBAL_LEDGER": str(self.mock_ledger),
        }
        self.orig_env = {k: os.environ.get(k) for k in self.env_patch}
        os.environ.update(self.env_patch)
        self.addCleanup(self._restore_env)

        self.manifest = load_manifest()

    def _restore_env(self) -> None:
        for k, v in self.orig_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_dry_run_leaves_no_traces(self) -> None:
        """Verify dry-run performs safety checks without modifying filesystem or creating ledger."""
        res = setup_global(
            manifest=self.manifest,
            requested_skills=["code-review", "git-hygiene"],
            dry_run=True,
            ledger_path=self.mock_ledger,
        )
        self.assertEqual(res, 0)
        self.assertFalse(self.mock_claude.exists())
        self.assertFalse(self.mock_agents.exists())
        self.assertFalse(self.mock_ledger.exists())

    def test_setup_shared_strategy_creates_symlinks_and_valid_frontmatter(self) -> None:
        """Verify setup_global creates directory symlinks for Claude Code and Shared Agent Skills."""
        res = setup_global(
            manifest=self.manifest,
            requested_skills=["code-review", "computer-vision"],
            strategy="shared",
            mode="link",
            ledger_path=self.mock_ledger,
        )
        self.assertEqual(res, 0)

        # Check Claude Code target
        claude_cr = self.mock_claude / "code-review"
        self.assertTrue(claude_cr.is_symlink())
        self.assertTrue((claude_cr / "SKILL.md").is_file())

        # Check Shared Agent Skills target (powers OpenCode and VS Code Copilot)
        agents_cr = self.mock_agents / "code-review"
        self.assertTrue(agents_cr.is_symlink())
        self.assertTrue((agents_cr / "SKILL.md").is_file())

        agents_cv = self.mock_agents / "computer-vision"
        self.assertTrue(agents_cv.is_symlink())
        self.assertTrue((agents_cv / "SKILL.md").is_file())

        # Verify YAML frontmatter validity in installed skills
        for target_dir in (self.mock_claude, self.mock_agents):
            for skill_id in ("code-review", "computer-vision"):
                skill_md = target_dir / skill_id / "SKILL.md"
                text = skill_md.read_text(encoding="utf-8")
                match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
                self.assertIsNotNone(match, f"Missing YAML frontmatter in {skill_md}")
                frontmatter = match.group(1)
                self.assertIn("name:", frontmatter)
                self.assertIn("description:", frontmatter)

        # Verify ledger structure
        ledger = read_global_ledger(self.mock_ledger)
        self.assertIn("claude-code", ledger["targets"])
        self.assertIn("shared-agents", ledger["targets"])
        self.assertIn("code-review", ledger["targets"]["claude-code"]["installs"])
        self.assertIn("code-review", ledger["targets"]["shared-agents"]["installs"])

    def test_all_three_agent_integrations_dedicated_strategy(self) -> None:
        """Verify dedicated strategy installs into Claude, OpenCode, and Copilot directories."""
        res = setup_global(
            manifest=self.manifest,
            requested_skills=["security-audit"],
            strategy="dedicated",
            mode="link",
            ledger_path=self.mock_ledger,
        )
        self.assertEqual(res, 0)

        # 1. Claude Code
        self.assertTrue((self.mock_claude / "security-audit" / "SKILL.md").is_file())
        # 2. OpenCode Dedicated
        self.assertTrue((self.mock_opencode / "security-audit" / "SKILL.md").is_file())
        # 3. GitHub Copilot Dedicated
        self.assertTrue((self.mock_copilot / "security-audit" / "SKILL.md").is_file())

        ledger = read_global_ledger(self.mock_ledger)
        self.assertIn("claude-code", ledger["targets"])
        self.assertIn("opencode", ledger["targets"])
        self.assertIn("copilot", ledger["targets"])

    def test_preservation_of_unmanaged_user_skills(self) -> None:
        """Verify unmanaged user skills are never deleted, overwritten, or modified."""
        # Pre-seed an unmanaged user skill
        unmanaged_dir = self.mock_agents / "my-custom-user-skill"
        unmanaged_dir.mkdir(parents=True, exist_ok=True)
        user_skill_md = unmanaged_dir / "SKILL.md"
        user_skill_md.write_text("---\nname: my-custom-user-skill\ndescription: Custom user skill\n---\n# User Notes\n")

        # Install Essentials skills globally
        setup_global(
            manifest=self.manifest,
            requested_skills=["git-hygiene"],
            strategy="shared",
            ledger_path=self.mock_ledger,
        )

        # Verify user skill is untouched
        self.assertTrue(user_skill_md.is_file())
        self.assertEqual(user_skill_md.read_text(), "---\nname: my-custom-user-skill\ndescription: Custom user skill\n---\n# User Notes\n")

        # Verify global-uninstall preserves user skill
        res = global_uninstall(
            uninstall_all=True,
            ledger_path=self.mock_ledger,
        )
        self.assertEqual(res, 0)
        self.assertTrue(user_skill_md.is_file(), "Unmanaged skill was unexpectedly removed!")

    def test_collision_with_unmanaged_skill_aborts_safely(self) -> None:
        """Verify naming collision with an unmanaged user skill aborts without overwriting."""
        # User manually created ~/.agents/skills/computer-vision
        collide_dir = self.mock_agents / "computer-vision"
        collide_dir.mkdir(parents=True, exist_ok=True)
        collide_file = collide_dir / "custom.txt"
        collide_file.write_text("Do not overwrite me!")

        # Attempt to install Essentials computer-vision
        res = setup_global(
            manifest=self.manifest,
            requested_skills=["computer-vision"],
            strategy="shared",
            ledger_path=self.mock_ledger,
        )
        self.assertEqual(res, 1, "Should have failed due to conflict")

        # Verify existing file was preserved
        self.assertTrue(collide_file.is_file())
        self.assertEqual(collide_file.read_text(), "Do not overwrite me!")
        self.assertFalse(self.mock_ledger.exists(), "Ledger should not be written on conflict")

    def test_global_sync_restores_missing_symlink(self) -> None:
        """Verify global-sync recreates missing symlinks recorded in ledger."""
        setup_global(
            manifest=self.manifest,
            requested_skills=["code-review"],
            strategy="shared",
            ledger_path=self.mock_ledger,
        )
        # Delete symlink on disk
        link_path = self.mock_agents / "code-review"
        link_path.unlink()
        self.assertFalse(link_path.exists())

        # Sync should repair it
        res = global_sync(manifest=self.manifest, ledger_path=self.mock_ledger)
        self.assertEqual(res, 0)
        self.assertTrue(link_path.is_symlink())
        self.assertTrue((link_path / "SKILL.md").is_file())

    def test_global_sync_preserves_user_modified_copy(self) -> None:
        """Verify global-sync never overwrites user modifications in copy mode."""
        setup_global(
            manifest=self.manifest,
            requested_skills=["code-review"],
            mode="copy",
            strategy="shared",
            ledger_path=self.mock_ledger,
        )
        installed_md = self.mock_agents / "code-review" / "SKILL.md"
        installed_md.write_text(installed_md.read_text() + "\n<!-- user customization -->\n")

        # Run sync
        res = global_sync(manifest=self.manifest, ledger_path=self.mock_ledger)
        self.assertEqual(res, 0)
        self.assertIn("<!-- user customization -->", installed_md.read_text())

    def test_selective_global_uninstall(self) -> None:
        """Verify uninstalling specific skills removes only requested items."""
        setup_global(
            manifest=self.manifest,
            requested_skills=["code-review", "git-hygiene"],
            strategy="shared",
            ledger_path=self.mock_ledger,
        )
        self.assertTrue((self.mock_agents / "code-review").exists())
        self.assertTrue((self.mock_agents / "git-hygiene").exists())

        # Uninstall only code-review
        res = global_uninstall(
            skill_ids=["code-review"],
            ledger_path=self.mock_ledger,
        )
        self.assertEqual(res, 0)
        self.assertFalse((self.mock_agents / "code-review").exists())
        self.assertTrue((self.mock_agents / "git-hygiene").exists())

        ledger = read_global_ledger(self.mock_ledger)
        self.assertNotIn("code-review", ledger["targets"]["shared-agents"]["installs"])
        self.assertIn("git-hygiene", ledger["targets"]["shared-agents"]["installs"])

    def test_corrupted_ledger_raises_helpful_error(self) -> None:
        """Verify corrupted ledger is caught and clear error returned."""
        self.mock_ledger.parent.mkdir(parents=True, exist_ok=True)
        self.mock_ledger.write_text("{corrupt-json")

        with self.assertRaises(GlobalManagerError) as ctx:
            read_global_ledger(self.mock_ledger)
        self.assertIn("Corrupt global ledger file", str(ctx.exception))

    def test_cli_integration_setup_global_and_status(self) -> None:
        """Verify CLI entrypoint works for setup-global, global-status, and global-uninstall."""
        # Test CLI setup-global
        ret = main(["setup-global", "engineering", "--dry-run"])
        self.assertEqual(ret, 0)

        # Test CLI setup-global actual install
        ret = main(["setup-global", "engineering"])
        self.assertEqual(ret, 0)
        self.assertTrue((self.mock_agents / "code-review").exists())

        # Test CLI global-status
        ret = main(["global-status", "--json"])
        self.assertEqual(ret, 0)

        # Test CLI global-uninstall
        ret = main(["global-uninstall", "--all", "--yes"])
        self.assertEqual(ret, 0)
        self.assertFalse((self.mock_agents / "code-review").exists())


if __name__ == "__main__":
    unittest.main()
