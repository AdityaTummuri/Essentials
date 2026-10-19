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

    def test_search_command(self) -> None:
        res = run_cli("search", "vision")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("computer-vision", res.stdout)

        res_json = run_cli("search", "audio", "--json")
        self.assertEqual(res_json.returncode, 0, res_json.stderr)
        data = json.loads(res_json.stdout)
        self.assertTrue(any(r["id"] == "browser-audio" for r in data))

    def test_inspect_command(self) -> None:
        res = run_cli("inspect", "computer-vision")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("SKILL: computer-vision", res.stdout)
        self.assertIn("robotics-ml", res.stdout)

        res_preset = run_cli("inspect", "robotics-ml")
        self.assertEqual(res_preset.returncode, 0, res_preset.stderr)
        self.assertIn("PRESET: robotics-ml", res_preset.stdout)
        self.assertIn("computer-vision", res_preset.stdout)

    def test_sync_command(self) -> None:
        # Install initial skill
        run_cli("install", "--skills", "computer-vision,browser-audio", "--target", str(self.target), "--agent", "cursor", "--yes")
        rule_cv = self.target / ".cursor" / "rules" / "computer-vision.mdc"
        rule_ba = self.target / ".cursor" / "rules" / "browser-audio.mdc"
        self.assertTrue(rule_cv.is_file())

        # Delete one file and locally modify the other
        rule_cv.unlink()
        rule_ba.write_text("locally modified rule\n")

        # Run sync
        res = run_cli("sync", "--target", str(self.target))
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertIn("restoring", res.stdout)
        self.assertIn("preserved without overwriting", res.stdout)
        self.assertTrue(rule_cv.is_file(), "deleted file should be restored by sync")
        self.assertEqual(rule_ba.read_text(), "locally modified rule\n", "modified rule must be preserved")

    def test_path_with_spaces(self) -> None:
        spaced_dir = self.tmp_dir / "my project with spaces"
        spaced_dir.mkdir()
        res = run_cli("install", "--skills", "code-review", "--target", str(spaced_dir), "--agent", "cursor", "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        self.assertTrue((spaced_dir / ".cursor" / "rules" / "code-review.mdc").is_file())

        res_un = run_cli("uninstall", "--target", str(spaced_dir), "--yes")
        self.assertEqual(res_un.returncode, 0, res_un.stderr + res_un.stdout)
        self.assertFalse((spaced_dir / ".cursor" / "rules" / "code-review.mdc").exists())

    def test_corrupted_ledger_recovery(self) -> None:
        ledger_file = self.target / ".essentials-ledger.json"
        ledger_file.write_text("NOT_VALID_JSON{:::}\n")
        res = run_cli("status", "--target", str(self.target))
        self.assertEqual(res.returncode, 2)
        self.assertIn("corrupt ledger file", res.stderr)
        self.assertIn("To reset, backup or remove this ledger", res.stderr)

    def test_new_presets_robotics_and_engineering(self) -> None:
        res = run_cli("install", "robotics-ml", "--target", str(self.target), "--agent", "cursor", "--yes")
        self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
        rules_dir = self.target / ".cursor" / "rules"
        for s in ("computer-vision", "model-evaluation", "dataset-curation", "edge-inference"):
            self.assertTrue((rules_dir / f"{s}.mdc").is_file(), f"{s} rule should be installed")


if __name__ == "__main__":
    unittest.main()

