"""End-to-end unit and integration tests for Essentials CLI."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = REPO_ROOT / "scripts" / "essentials"


def run_cli(*args: str, stdin: str = "") -> subprocess.CompletedProcess:
    """Helper to run the CLI executable."""
    return subprocess.run(
        [str(CLI_PATH), *args],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=120,
    )


class EssentialsCLITests(unittest.TestCase):
    """Test suite for the Essentials CLI across multi-agent targets."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_dir = Path(self._tmp.name)
        self.target = self.tmp_dir / "test-project"
        self.target.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # ----- Read-only commands

    def test_list_command(self) -> None:
        res = run_cli("list")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("ESSENTIALS: Universal AI Developer Toolkit", res.stdout)
        self.assertIn("portfolio", res.stdout)
        self.assertIn("dashboard", res.stdout)
        self.assertIn("python-dev", res.stdout)
        self.assertIn("claude-code", res.stdout)
        self.assertIn("cursor", res.stdout)
        self.assertIn("oil-motion", res.stdout)

    def test_list_json(self) -> None:
        res = run_cli("list", "--json")
        self.assertEqual(res.returncode, 0, res.stderr)
        data = json.loads(res.stdout)
        self.assertIn("presets", data)
        self.assertIn("installable", data)
        self.assertIn("supportedAgents", data)
        self.assertIn("claude-code", data["supportedAgents"])
        self.assertIn("cursor", data["supportedAgents"])

    def test_validate_command(self) -> None:
        res = run_cli("validate")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertIn("0 error(s)", res.stdout)
        self.assertIn("0 warning(s)", res.stdout)

    # ----- Dry-run

    def test_install_dry_run_modifies_nothing(self) -> None:
        before = sorted(os.listdir(self.target))
        res = run_cli("install", "dashboard", "--target", str(self.target), "--dry-run")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertIn("Dry run: no files changed.", res.stdout)
        self.assertEqual(sorted(os.listdir(self.target)), before)

    # ----- Multi-Agent Installations

    def test_install_claude_code_symlink(self) -> None:
        res = run_cli("install", "dashboard", "--target", str(self.target), "--agent", "claude-code", "--mode", "link", "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        skills_dir = self.target / ".claude" / "skills"
        self.assertTrue(skills_dir.is_dir())
        self.assertTrue((skills_dir / "frontend-design").is_symlink())
        self.assertTrue((skills_dir / "frontend-design" / "SKILL.md").is_file())

        # Check ledger
        ledger = json.loads((self.target / ".essentials-ledger.json").read_text())
        self.assertIn("frontend-design", ledger["installs"])
        self.assertEqual(ledger["installs"]["frontend-design"]["mode"], "link")
        self.assertEqual(ledger["installs"]["frontend-design"]["agent"], "claude-code")

    def test_install_cursor_rules(self) -> None:
        res = run_cli("install", "--skills", "code-review,frontend-design", "--target", str(self.target), "--agent", "cursor", "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        rule_file = self.target / ".cursor" / "rules" / "code-review.mdc"
        self.assertTrue(rule_file.is_file())
        content = rule_file.read_text(encoding="utf-8")
        self.assertIn("description:", content)
        self.assertIn("globs: *", content)
        self.assertIn("alwaysApply: false", content)

    def test_install_windsurf_rules(self) -> None:
        res = run_cli("install", "--skills", "code-review", "--target", str(self.target), "--agent", "windsurf", "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        rule_file = self.target / ".windsurf" / "rules" / "code-review.md"
        self.assertTrue(rule_file.is_file())
        content = rule_file.read_text(encoding="utf-8")
        self.assertIn("# Rule: code-review", content)

    def test_install_codex_and_gemini(self) -> None:
        res = run_cli("install", "--skills", "git-hygiene", "--target", str(self.target), "--agent", "gemini-cli", "--mode", "copy", "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        skill_dir = self.target / ".agents" / "skills" / "git-hygiene"
        self.assertTrue(skill_dir.is_dir())
        self.assertFalse(skill_dir.is_symlink())
        self.assertTrue((skill_dir / "SKILL.md").is_file())

    def test_install_copilot_prompts(self) -> None:
        res = run_cli("install", "--skills", "git-hygiene", "--target", str(self.target), "--agent", "copilot", "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        prompt_file = self.target / ".github" / "prompts" / "git-hygiene.prompt.md"
        self.assertTrue(prompt_file.is_file())

    # ----- Status & Conflict Protection

    def test_status_reports_correct_state(self) -> None:
        run_cli("install", "--skills", "code-review", "--target", str(self.target), "--agent", "cursor", "--yes")
        res = run_cli("status", "--target", str(self.target))
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("code-review", res.stdout)
        self.assertIn("[OK]", res.stdout)

    def test_conflict_aborts_without_modification(self) -> None:
        # Pre-create an unmanaged file where Cursor rule would be installed
        rule_dir = self.target / ".cursor" / "rules"
        rule_dir.mkdir(parents=True)
        unmanaged_file = rule_dir / "code-review.mdc"
        unmanaged_file.write_text("unmanaged user rule\n")

        res = run_cli("install", "--skills", "code-review", "--target", str(self.target), "--agent", "cursor", "--yes")
        self.assertEqual(res.returncode, 1)
        self.assertIn("Installation aborted due to conflicts", res.stderr)
        self.assertEqual(unmanaged_file.read_text(), "unmanaged user rule\n")

    # ----- Uninstall & Modification Protection

    def test_uninstall_clean(self) -> None:
        run_cli("install", "--skills", "code-review,git-hygiene", "--target", str(self.target), "--agent", "cursor", "--yes")
        res = run_cli("uninstall", "--target", str(self.target), "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertFalse((self.target / ".cursor" / "rules" / "code-review.mdc").exists())
        self.assertFalse((self.target / ".cursor" / "rules" / "git-hygiene.mdc").exists())
        self.assertFalse((self.target / ".essentials-ledger.json").exists())

    def test_uninstall_preserves_user_modified_files(self) -> None:
        run_cli("install", "--skills", "code-review,git-hygiene", "--target", str(self.target), "--agent", "cursor", "--yes")
        # Modify code-review rule locally
        target_file = self.target / ".cursor" / "rules" / "code-review.mdc"
        target_file.write_text("locally modified rule\n")

        res = run_cli("uninstall", "--target", str(self.target), "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertTrue(target_file.is_file(), "modified user file must be preserved")
        self.assertFalse((self.target / ".cursor" / "rules" / "git-hygiene.mdc").exists(), "unmodified file should be removed")

        # Ledger should keep record of modified file
        ledger = json.loads((self.target / ".essentials-ledger.json").read_text())
        self.assertIn("code-review", ledger["installs"])
        self.assertNotIn("git-hygiene", ledger["installs"])

    # ----- Safety Guards

    def test_refuses_to_install_into_essentials_repo(self) -> None:
        res = run_cli("install", "dashboard", "--target", str(REPO_ROOT), "--yes")
        self.assertEqual(res.returncode, 2)
        self.assertIn("refusing to install into the Essentials repository itself", res.stderr)

    def test_unknown_skill_rejected(self) -> None:
        res = run_cli("install", "--skills", "nonexistent-skill-id", "--target", str(self.target), "--yes")
        self.assertEqual(res.returncode, 2)
        self.assertIn("not installable", res.stderr)


if __name__ == "__main__":
    unittest.main()
