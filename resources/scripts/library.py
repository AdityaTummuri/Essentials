#!/usr/bin/env python3
"""Install, uninstall, list, and validate Claude Code skills from this library.

Installs go into <project>/.claude/skills/<id>, as a symlink (default) or a copy.
Every install is recorded in <project>/.claude/.resources-library.json so that
uninstall removes only what this tool created. Stdlib only.

Run through scripts/setup-project.sh rather than directly.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

LIBRARY = Path(__file__).resolve().parent.parent
MANIFEST = LIBRARY / "resources.json"
LEDGER_NAME = ".resources-library.json"
REVIEW_STATUSES = {"static-reviewed", "needs-review", "needs-decision", "not-applicable"}
# Files that would change Claude Code behaviour when vendored. Never allowed in the library.
FORBIDDEN_NAMES = {"settings.json", "settings.local.json", "hooks.json", ".mcp.json", "plugin.json"}
FORBIDDEN_DIRS = {".claude-plugin", ".git"}


class ToolError(Exception):
    pass


# --------------------------------------------------------------------------- helpers

def load_manifest() -> dict:
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ToolError(f"cannot read {MANIFEST}: {exc}") from exc


def installable(manifest: dict) -> dict[str, dict]:
    return {r["id"]: r for r in manifest["resources"] if r.get("installable")}


def frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fields: dict[str, str] = {}
    if match:
        for line in match.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "\t")):
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip('"')
    return fields


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> str:
    """Hash every file's relative path and contents, in sorted order."""
    digest = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames):
            full = Path(dirpath) / name
            digest.update(str(full.relative_to(root)).encode())
            digest.update(sha256_file(full).encode())
    return digest.hexdigest()


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def ask(prompt: str) -> str:
    return input(prompt).strip()


# --------------------------------------------------------------------------- project inspection

def project_dir(arg: str) -> Path:
    path = Path(arg).expanduser().resolve()
    if not path.is_dir():
        raise ToolError(f"project directory does not exist: {path}")
    if path == LIBRARY or LIBRARY in path.parents:
        raise ToolError("refusing to install into the library itself")
    return path


def ledger_path(project: Path) -> Path:
    return project / ".claude" / LEDGER_NAME


def read_ledger(project: Path) -> dict:
    path = ledger_path(project)
    if not path.exists():
        return {"installs": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ToolError(f"cannot read ledger {path}: {exc}") from exc
    data.setdefault("installs", {})
    return data


def write_ledger(project: Path, ledger: dict) -> None:
    path = ledger_path(project)
    if not ledger["installs"]:
        if path.exists():
            path.unlink()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def global_skill_names() -> set[str]:
    """Read-only: names of skills that user-level installs already provide."""
    names: set[str] = set()
    base = Path.home() / ".claude" / "skills"
    roots = [base] + [p for p in base.glob("synced/*") if p.is_dir()] if base.is_dir() else []
    for root in roots:
        try:
            names.update(p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
        except OSError:
            continue
    names.discard("synced")
    return names


def inspect_project(project: Path) -> None:
    claude = project / ".claude"
    print(f"Project: {project}")
    print(f"  CLAUDE.md:               {'present (not modified)' if (project / 'CLAUDE.md').exists() else 'absent'}")
    for name in ("settings.json", "settings.local.json"):
        path = claude / name
        if path.exists():
            hooks = "defines hooks" if '"hooks"' in path.read_text(encoding="utf-8", errors="replace") else "no hooks key"
            print(f"  .claude/{name}: present, {hooks} (not modified)")
        else:
            print(f"  .claude/{name}: absent")
    skills = claude / "skills"
    existing = sorted(p.name for p in skills.iterdir()) if skills.is_dir() else []
    print(f"  .claude/skills/:         {len(existing)} entries" + (f": {', '.join(existing)}" if existing else ""))
    ledger = read_ledger(project)["installs"]
    print(f"  managed by this tool:    {len(ledger)} install(s)" + (f": {', '.join(sorted(ledger))}" if ledger else ""))


# --------------------------------------------------------------------------- selection

def resolve_selection(manifest: dict, presets: list[str], ids: list[str]) -> list[dict]:
    available = installable(manifest)
    chosen: list[str] = []
    for preset in presets:
        if preset not in manifest["presets"]:
            raise ToolError(f"unknown preset '{preset}'. Known: {', '.join(manifest['presets'])}")
        chosen.extend(manifest["presets"][preset]["skills"])
    chosen.extend(ids)
    unknown = [i for i in chosen if i not in available]
    if unknown:
        raise ToolError(f"not installable (unknown or not vendored): {', '.join(unknown)}")
    seen: dict[str, dict] = {}
    for skill_id in chosen:
        seen.setdefault(skill_id, available[skill_id])
    return list(seen.values())


def print_catalogue(manifest: dict) -> None:
    grouped: dict[str, list[dict]] = {}
    for resource in installable(manifest).values():
        grouped.setdefault(resource["category"], []).append(resource)
    index = 0
    print("Available skills (number, id, purpose):")
    for category in manifest["categories"]:
        if category not in grouped:
            continue
        print(f"\n  [{category}] {manifest['categories'][category]}")
        for resource in grouped[category]:
            index += 1
            print(f"   {index:>2}. {resource['id']:<30} {resource['useCases']}")
    print("\nPresets:")
    for name, preset in manifest["presets"].items():
        print(f"   {name:<12} {preset['description']} ({len(preset['skills'])} skills)")


def interactive_selection(manifest: dict) -> tuple[list[str], list[str]]:
    print_catalogue(manifest)
    order = [r["id"] for c in manifest["categories"] for r in installable(manifest).values() if r["category"] == c]
    answer = ask("\nPreset name, or comma-separated ids/numbers, blank to cancel: ")
    if not answer:
        return [], []
    presets: list[str] = []
    ids: list[str] = []
    for token in (t.strip() for t in answer.split(",") if t.strip()):
        if token in manifest["presets"]:
            presets.append(token)
        elif token.isdigit() and 1 <= int(token) <= len(order):
            ids.append(order[int(token) - 1])
        else:
            ids.append(token)
    return presets, ids


# --------------------------------------------------------------------------- setup

def plan_setup(project: Path, selected: list[dict], ledger: dict) -> tuple[list[tuple[dict, Path]], list[str], list[str]]:
    skills_dir = project / ".claude" / "skills"
    to_install: list[tuple[dict, Path]] = []
    conflicts: list[str] = []
    notes: list[str] = []
    global_names = global_skill_names()
    for resource in selected:
        skill_id = resource["id"]
        dest = skills_dir / skill_id
        if skill_id in ledger["installs"]:
            if dest.exists() or dest.is_symlink():
                notes.append(f"{skill_id}: already installed by this tool, skipped")
            else:
                notes.append(f"{skill_id}: recorded as installed but missing; run --uninstall to clear the record")
            continue
        if os.path.lexists(dest):
            conflicts.append(f"{skill_id}: {dest} already exists and was not created by this tool")
            continue
        if skill_id in global_names:
            notes.append(f"{skill_id}: a user-level skill with this name exists; the project copy will take precedence here")
        to_install.append((resource, dest))
    return to_install, conflicts, notes


def run_setup(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    project = project_dir(args.project)
    inspect_project(project)
    print()

    presets, ids = list(args.preset or []), list(args.skills or [])
    if not presets and not ids:
        if not sys.stdin.isatty():
            raise ToolError("no selection given. Pass --preset or --skills (see --list)")
        presets, ids = interactive_selection(manifest)
        if not presets and not ids:
            print("Nothing selected. No changes made.")
            return 0

    selected = resolve_selection(manifest, presets, ids)
    ledger = read_ledger(project)
    to_install, conflicts, notes = plan_setup(project, selected, ledger)

    if conflicts:
        print("Conflicts (nothing was changed):")
        for line in conflicts:
            print(f"  ! {line}")
        print("Remove or rename the conflicting entries, or deselect them, then run again.")
        return 1

    mode = args.mode
    print(f"Mode: {mode}" + ("  (symlinks use absolute paths; use --mode copy for repos shared with others)" if mode == "link" else ""))
    print("Planned changes:")
    for resource, dest in to_install:
        print(f"  + {mode:<4} {resource['id']:<30} -> {dest}")
    for line in notes:
        print(f"  . {line}")
    if not to_install:
        print("  (nothing new to install)")
        return 0

    if args.dry_run:
        print("\nDry run: no files changed.")
        return 0
    if not args.yes:
        if not sys.stdin.isatty() or ask("Proceed? [y/N] ").lower() != "y":
            print("Cancelled. No changes made.")
            return 1

    skills_dir = project / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    for resource, dest in to_install:
        source = (LIBRARY / resource["path"]).resolve()
        if mode == "link":
            os.symlink(source, dest, target_is_directory=True)
        else:
            shutil.copytree(source, dest, symlinks=False)
        ledger["installs"][resource["id"]] = {
            "mode": mode,
            "source": str(source),
            "sha256": sha256_file(source / "SKILL.md"),
            "treeSha256": tree_digest(source),
            "installedAt": now(),
        }
    write_ledger(project, ledger)

    print("\nVerifying:")
    failures = 0
    for resource, dest in to_install:
        ok, detail = verify_install(resource, dest, ledger["installs"][resource["id"]])
        failures += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'} {resource['id']}: {detail}")
    print(f"\nInstalled {len(to_install) - failures} of {len(to_install)} into {skills_dir}.")
    print(f"Ledger: {ledger_path(project)} (keep it, so --uninstall can find these installs)")
    print("Use: type /<skill-id> in Claude Code, or describe the task and Claude loads matching skills.")
    return 1 if failures else 0


def verify_install(resource: dict, dest: Path, record: dict) -> tuple[bool, str]:
    skill_md = dest / "SKILL.md"
    if not skill_md.is_file():
        return False, "SKILL.md missing"
    fields = frontmatter(skill_md)
    if fields.get("name") != resource["id"]:
        return False, f"frontmatter name '{fields.get('name')}' does not match id"
    if record["mode"] == "link" and os.readlink(dest) != record["source"]:
        return False, "symlink target is not the library source"
    if sha256_file(skill_md) != resource["skillMd"]["sha256"]:
        return False, "SKILL.md differs from the manifest hash"
    return True, f"{record['mode']} -> {record['source']}"


# --------------------------------------------------------------------------- uninstall

def run_uninstall(args: argparse.Namespace) -> int:
    project = project_dir(args.project)
    ledger = read_ledger(project)
    if not ledger["installs"]:
        print(f"Nothing to uninstall: no records in {ledger_path(project)}.")
        return 0

    removable: list[str] = []
    kept: list[str] = []
    for skill_id, record in sorted(ledger["installs"].items()):
        dest = project / ".claude" / "skills" / skill_id
        if not os.path.lexists(dest):
            kept.append(f"{skill_id}: already gone; record will be cleared")
            removable.append(skill_id)
        elif record["mode"] == "link":
            if dest.is_symlink() and os.readlink(dest) == record["source"]:
                removable.append(skill_id)
            else:
                kept.append(f"{skill_id}: link was replaced or changed; left in place")
        else:
            if dest.is_dir() and not dest.is_symlink() and tree_digest(dest) == record["treeSha256"]:
                removable.append(skill_id)
            else:
                kept.append(f"{skill_id}: copy was modified since install; left in place")

    print(f"Uninstall plan for {project}:")
    for skill_id in removable:
        print(f"  - remove {skill_id}")
    for line in kept:
        print(f"  . {line}")
    if args.dry_run:
        print("\nDry run: no files changed.")
        return 0
    if not removable:
        return 0
    if not args.yes:
        if not sys.stdin.isatty() or ask("Proceed? [y/N] ").lower() != "y":
            print("Cancelled. No changes made.")
            return 1

    for skill_id in removable:
        dest = project / ".claude" / "skills" / skill_id
        if os.path.lexists(dest):
            if dest.is_symlink():
                dest.unlink()
            else:
                shutil.rmtree(dest)
        del ledger["installs"][skill_id]
    write_ledger(project, ledger)
    print(f"Removed {len(removable)} install(s). {len(ledger['installs'])} record(s) kept.")
    return 0


# --------------------------------------------------------------------------- list and validate

def run_list(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    print_catalogue(manifest)
    held = [r for r in manifest["resources"] if not r.get("installable")]
    if held:
        print("\nNot installable (held, catalogue, dependency, or mod):")
        for resource in held:
            print(f"   {resource['id']:<30} {resource['status']:<18} {resource['description'][:70]}")
    return 0


def run_validate(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    errors: list[str] = []
    warnings: list[str] = []
    resources = manifest["resources"]

    if manifest.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    ids = [r["id"] for r in resources]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"duplicate id: {dup}")

    for resource in resources:
        rid = resource["id"]
        if resource.get("securityReview", {}).get("status") not in REVIEW_STATUSES:
            errors.append(f"{rid}: securityReview.status must be one of {sorted(REVIEW_STATUSES)}")
        if not resource.get("installable"):
            if resource.get("path") and resource["kind"] == "skill":
                errors.append(f"{rid}: held skill must not have a path in the library")
            continue
        if resource.get("status") != "vendored":
            errors.append(f"{rid}: installable entries must have status 'vendored'")
        path = LIBRARY / resource["path"]
        if not (path / "SKILL.md").is_file():
            errors.append(f"{rid}: {path}/SKILL.md is missing")
            continue
        fields = frontmatter(path / "SKILL.md")
        if fields.get("name") != rid:
            errors.append(f"{rid}: frontmatter name '{fields.get('name')}' does not match id")
        if not fields.get("description"):
            errors.append(f"{rid}: frontmatter description is empty")
        if sha256_file(path / "SKILL.md") != resource.get("skillMd", {}).get("sha256"):
            errors.append(f"{rid}: SKILL.md changed since the manifest was generated")
        collection = LIBRARY / "skills" / resource["collection"]
        if not any(collection.glob("LICENSE*")):
            errors.append(f"{rid}: no LICENSE file in {collection.relative_to(LIBRARY)}")
        if not (collection / "SOURCE.md").is_file():
            errors.append(f"{rid}: no SOURCE.md in {collection.relative_to(LIBRARY)}")
        for dirpath, dirnames, filenames in os.walk(path):
            for name in filenames:
                if name in FORBIDDEN_NAMES:
                    errors.append(f"{rid}: forbidden file {Path(dirpath, name).relative_to(LIBRARY)}")
            for name in dirnames:
                if name in FORBIDDEN_DIRS:
                    errors.append(f"{rid}: forbidden directory {Path(dirpath, name).relative_to(LIBRARY)}")
            for name in filenames + dirnames:
                if Path(dirpath, name).is_symlink():
                    errors.append(f"{rid}: symlink inside library {Path(dirpath, name).relative_to(LIBRARY)}")

    known = {r["id"] for r in resources if r.get("installable")}
    for name, preset in manifest["presets"].items():
        for skill_id in preset["skills"]:
            if skill_id not in known:
                errors.append(f"preset '{name}' references non-installable or unknown id '{skill_id}'")

    listed = {r["path"] for r in resources if r.get("path")}
    for skill_md in (LIBRARY / "skills").rglob("SKILL.md"):
        rel = str(skill_md.parent.relative_to(LIBRARY))
        if rel not in listed:
            warnings.append(f"{rel} is not in resources.json")

    for line in errors:
        print(f"ERROR   {line}")
    for line in warnings:
        print(f"WARNING {line}")
    print(f"\n{len(known)} installable skills, {len(manifest['presets'])} presets, "
          f"{len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


# --------------------------------------------------------------------------- CLI

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("project", nargs="?", help="project directory to install into")
    parser.add_argument("--preset", action="append", help="install a preset (repeatable)")
    parser.add_argument("--skills", type=lambda s: [x for x in s.split(",") if x], action="append",
                        help="comma-separated skill ids to install (repeatable)")
    parser.add_argument("--mode", choices=["link", "copy"], default="link", help="symlink (default) or copy")
    parser.add_argument("--dry-run", action="store_true", help="show what would change; change nothing")
    parser.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    parser.add_argument("--uninstall", action="store_true", help="remove installs recorded for this project")
    parser.add_argument("--list", action="store_true", help="list skills, presets, and held resources")
    parser.add_argument("--validate", action="store_true", help="check the library against resources.json")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.skills = [s for group in (args.skills or []) for s in group]
    try:
        if args.validate:
            return run_validate(args)
        if args.list:
            return run_list(args)
        if not args.project:
            parser.error("a project directory is required (or use --list / --validate)")
        if args.uninstall:
            return run_uninstall(args)
        return run_setup(args)
    except ToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\ninterrupted; no further changes made", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
