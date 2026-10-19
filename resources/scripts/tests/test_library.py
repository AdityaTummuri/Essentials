"""End-to-end tests for scripts/setup-project.sh.

Runs the installer against temporary project directories only. Never touches a real
project or the user's ~/.claude. Run with:

    python3 -I -m unittest discover -s scripts/tests -v
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

LIBRARY = Path(__file__).resolve().parents[2]
WRAPPER = LIBRARY / "scripts" / "setup-project.sh"
LEDGER = Path(".claude") / ".resources-library.json"


def run(*args: str, stdin: str = "") -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(WRAPPER), *args],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=120,
    )


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.project = self.root / "project"
        self.project.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # ----- read-only commands

    def test_validate_passes_on_library(self) -> None:
        result = run("--validate")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_list_shows_presets_and_held_items(self) -> None:
        result = run("--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("portfolio", result.stdout)
        self.assertIn("impeccable", result.stdout)

    # ----- dry run

    def test_dry_run_changes_nothing(self) -> None:
        before = sorted(p.name for p in self.project.iterdir())
        result = run(str(self.project), "--preset", "portfolio", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Dry run: no files changed.", result.stdout)
        self.assertEqual(sorted(p.name for p in self.project.iterdir()), before)
        self.assertFalse((self.project / ".claude").exists())

    # ----- link install

    def test_link_install_preset_verifies_and_records(self) -> None:
        result = run(str(self.project), "--preset", "dashboard", "--yes")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        skills = self.project / ".claude" / "skills"
        for skill_id in ("frontend-design", "ui-ux-pro-max", "design", "design-md",
                         "animation-performance", "review-animations"):
            link = skills / skill_id
            self.assertTrue(link.is_symlink(), skill_id)
            self.assertTrue((link / "SKILL.md").is_file(), skill_id)
        ledger = json.loads((self.project / LEDGER).read_text())
        self.assertEqual(len(ledger["installs"]), 6)
        self.assertEqual(ledger["installs"]["design-md"]["mode"], "link")

    def test_rerun_is_a_no_op(self) -> None:
        run(str(self.project), "--skills", "animate", "--yes")
        result = run(str(self.project), "--skills", "animate", "--yes")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("(nothing new to install)", result.stdout)
        self.assertIn("already installed by this tool", result.stdout)

    def test_uninstall_removes_only_recorded_links(self) -> None:
        run(str(self.project), "--skills", "animate,threejs-scene", "--yes")
        unrelated = self.project / ".claude" / "skills" / "my-own-skill"
        unrelated.mkdir(parents=True)
        (unrelated / "SKILL.md").write_text("---\nname: my-own-skill\ndescription: mine\n---\n")

        result = run(str(self.project), "--uninstall", "--yes")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(os.path.lexists(self.project / ".claude" / "skills" / "animate"))
        self.assertFalse(os.path.lexists(self.project / ".claude" / "skills" / "threejs-scene"))
        self.assertTrue(unrelated.is_dir(), "unrelated user skill must survive uninstall")
        self.assertFalse((self.project / LEDGER).exists(), "empty ledger should be removed")

    # ----- copy install

    def test_copy_install_then_modified_copy_is_kept(self) -> None:
        result = run(str(self.project), "--skills", "threejs-scene,threejs-lighting", "--mode", "copy", "--yes")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        scene = self.project / ".claude" / "skills" / "threejs-scene"
        self.assertFalse(scene.is_symlink())
        self.assertEqual(digest_file(scene / "SKILL.md"),
                         digest_file(LIBRARY / "skills/threejs/cesartevisual-threejs-skills/threejs-scene/SKILL.md"))

        (scene / "SKILL.md").write_text("locally edited\n")
        result = run(str(self.project), "--uninstall", "--yes")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(scene.is_dir(), "modified copy must not be deleted")
        self.assertFalse((self.project / ".claude" / "skills" / "threejs-lighting").exists())
        ledger = json.loads((self.project / LEDGER).read_text())
        self.assertEqual(list(ledger["installs"]), ["threejs-scene"])

    # ----- safety

    def test_conflict_aborts_before_any_change(self) -> None:
        existing = self.project / ".claude" / "skills" / "animate"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("user's own skill\n")
        result = run(str(self.project), "--skills", "animate,threejs-scene", "--yes")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Conflicts (nothing was changed)", result.stdout)
        self.assertFalse(os.path.lexists(self.project / ".claude" / "skills" / "threejs-scene"))
        self.assertEqual((existing / "SKILL.md").read_text(), "user's own skill\n")
        self.assertFalse((self.project / LEDGER).exists())

    def test_existing_project_config_is_never_modified(self) -> None:
        claude = self.project / ".claude"
        claude.mkdir()
        settings = claude / "settings.json"
        settings.write_text('{"permissions": {"defaultMode": "auto"}}\n')
        claude_md = self.project / "CLAUDE.md"
        claude_md.write_text("# my rules\n")
        before = {p: digest_file(p) for p in (settings, claude_md)}
        result = run(str(self.project), "--skills", "animate", "--yes")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual({p: digest_file(p) for p in (settings, claude_md)}, before)

    def test_refuses_to_run_without_selection_when_not_a_tty(self) -> None:
        result = run(str(self.project))
        self.assertEqual(result.returncode, 2)
        self.assertIn("no selection given", result.stderr)

    def test_unknown_skill_id_is_rejected(self) -> None:
        result = run(str(self.project), "--skills", "does-not-exist", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not installable", result.stderr)
        self.assertFalse((self.project / ".claude").exists())

    def test_held_skill_cannot_be_installed(self) -> None:
        result = run(str(self.project), "--skills", "impeccable", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("impeccable", result.stderr)

    def test_refuses_to_install_into_the_library(self) -> None:
        result = run(str(LIBRARY / "skills"), "--skills", "animate", "--dry-run")
        self.assertEqual(result.returncode, 2)
        self.assertIn("refusing to install into the library", result.stderr)

    def test_missing_project_directory_is_rejected(self) -> None:
        result = run(str(self.root / "nope"), "--skills", "animate", "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("does not exist", result.stderr)


class ValidationTests(unittest.TestCase):
    """Validation must catch a tampered vendored file. Works on a copy, never on the library."""

    def test_tampered_skill_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "lib"
            shutil.copytree(LIBRARY / "skills", copy / "skills")
            shutil.copytree(LIBRARY / "scripts", copy / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copy(LIBRARY / "resources.json", copy / "resources.json")
            target = copy / "skills/motion/emil-design-eng/animate/SKILL.md"
            target.write_bytes(target.read_bytes() + b"\n<!-- tamper -->\n")
            result = subprocess.run(
                ["python3", "-I", str(copy / "scripts/library.py"), "--validate"],
                capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("changed since the manifest was generated", result.stdout)


if __name__ == "__main__":
    unittest.main()
