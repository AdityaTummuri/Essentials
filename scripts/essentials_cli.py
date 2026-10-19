#!/usr/bin/env python3
"""Essentials CLI: Universal AI Developer Toolkit manager.

Install, uninstall, inspect, list, and validate AI agent skills across
Claude Code, Gemini CLI, Cursor, OpenAI Codex, Windsurf, and Copilot.
Standard library only.
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
from typing import Any

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from adapters.base import BaseAdapter, sha256_file, tree_digest
from adapters.registry import get_adapter, list_adapters, supported_agent_names

MANIFEST_PATH = REPO_ROOT / "resources" / "resources.json"
LEDGER_NAME = ".essentials-ledger.json"
LEGACY_LEDGER_PATH = Path(".claude") / ".resources-library.json"

REVIEW_STATUSES = {"static-reviewed", "needs-review", "needs-decision", "not-applicable"}
FORBIDDEN_NAMES = {"settings.json", "settings.local.json", "hooks.json", ".mcp.json", "plugin.json"}
FORBIDDEN_DIRS = {".claude-plugin", ".git"}


class CLIError(Exception):
    """Raised for expected user-facing CLI errors."""
    pass


# --------------------------------------------------------------------------- Manifest & Helpers

def load_manifest() -> dict[str, Any]:
    """Load and parse the resources.json manifest."""
    if not MANIFEST_PATH.is_file():
        raise CLIError(f"manifest not found at {MANIFEST_PATH}")
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CLIError(f"cannot read manifest: {exc}") from exc


def get_installable_resources(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return map of installable skill id -> resource dict."""
    return {
        r["id"]: r
        for r in manifest.get("resources", [])
        if r.get("installable")
    }


def now_iso() -> str:
    """Return current UTC ISO-8601 timestamp."""
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def ask_confirmation(prompt: str) -> bool:
    """Prompt user for confirmation in interactive sessions."""
    if not sys.stdin.isatty():
        return False
    try:
        ans = input(prompt).strip().lower()
        return ans in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


def resolve_project_dir(arg: str | None) -> Path:
    """Resolve and validate a target project directory."""
    if not arg:
        raise CLIError("a target project directory is required (pass --target <dir> or specify path)")
    path = Path(arg).expanduser().resolve()
    if not path.is_dir():
        raise CLIError(f"target directory does not exist: {path}")
    if path == REPO_ROOT or REPO_ROOT in path.parents:
        raise CLIError("refusing to install into the Essentials repository itself")
    return path


# --------------------------------------------------------------------------- Ledger Management

def read_project_ledger(project: Path) -> dict[str, Any]:
    """Read the installation ledger, supporting modern and legacy formats."""
    ledger_file = project / LEDGER_NAME
    if ledger_file.is_file():
        try:
            data = json.loads(ledger_file.read_text(encoding="utf-8"))
            data.setdefault("installs", {})
            return data
        except Exception as exc:
            raise CLIError(f"corrupt ledger file {ledger_file}: {exc}. To reset, backup or remove this ledger.") from exc

    # Check for legacy Claude Code ledger
    legacy_file = project / LEGACY_LEDGER_PATH
    if legacy_file.is_file():
        try:
            legacy_data = json.loads(legacy_file.read_text(encoding="utf-8"))
            installs = {}
            for sid, rec in legacy_data.get("installs", {}).items():
                installs[sid] = {
                    "agent": "claude-code",
                    "mode": rec.get("mode", "link"),
                    "source": rec.get("source", ""),
                    "destination": f".claude/skills/{sid}",
                    "sha256": rec.get("sha256", ""),
                    "treeSha256": rec.get("treeSha256", ""),
                    "installedAt": rec.get("installedAt", ""),
                }
            return {"installs": installs}
        except Exception:
            pass

    return {"installs": {}}


def write_project_ledger(project: Path, ledger: dict[str, Any]) -> None:
    """Write project installation ledger atomically."""
    ledger_file = project / LEDGER_NAME
    if not ledger["installs"]:
        if ledger_file.exists():
            ledger_file.unlink()
        legacy_file = project / LEGACY_LEDGER_PATH
        if legacy_file.exists():
            legacy_file.unlink()
        return

    tmp = ledger_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, ledger_file)

    # If any claude-code installs exist, mirror to legacy ledger for backward compat
    claude_installs = {
        sid: {
            "mode": rec.get("mode", "link"),
            "source": rec.get("source", ""),
            "sha256": rec.get("sha256", ""),
            "treeSha256": rec.get("treeSha256", ""),
            "installedAt": rec.get("installedAt", ""),
        }
        for sid, rec in ledger["installs"].items()
        if rec.get("agent") in ("claude", "claude-code")
    }
    legacy_file = project / LEGACY_LEDGER_PATH
    if claude_installs:
        legacy_file.parent.mkdir(parents=True, exist_ok=True)
        leg_tmp = legacy_file.with_suffix(".tmp")
        leg_tmp.write_text(json.dumps({"installs": claude_installs}, indent=2) + "\n", encoding="utf-8")
        os.replace(leg_tmp, legacy_file)
    elif legacy_file.exists():
        legacy_file.unlink()


# --------------------------------------------------------------------------- Command: List

def cmd_list(args: argparse.Namespace) -> int:
    """List available skills, presets, supported agents, and held items."""
    manifest = load_manifest()
    installable = get_installable_resources(manifest)

    if getattr(args, "json", False):
        print(json.dumps({
            "presets": manifest.get("presets", {}),
            "installable": list(installable.values()),
            "held": [r for r in manifest.get("resources", []) if not r.get("installable")],
            "supportedAgents": supported_agent_names(),
        }, indent=2))
        return 0

    print("=" * 78)
    print(" ESSENTIALS: Universal AI Developer Toolkit")
    print("=" * 78)

    print("\n📦 Available Presets:")
    for name, pdata in manifest.get("presets", {}).items():
        skills_count = len(pdata.get("skills", []))
        print(f"  • {name:<14} {pdata.get('description', '')} ({skills_count} skills)")

    print("\n🤖 Supported Target Agents:")
    for adapter in list_adapters():
        aliases = f" (aliases: {', '.join(adapter.aliases)})" if adapter.aliases else ""
        print(f"  • {adapter.name:<14} {adapter.description}{aliases}")

    grouped: dict[str, list[dict[str, Any]]] = {}
    for res in installable.values():
        grouped.setdefault(res.get("category", "general"), []).append(res)

    print("\n🛠️ Installable Skills by Category:")
    for cat, desc in manifest.get("categories", {}).items():
        skills = grouped.get(cat, [])
        if not skills:
            continue
        print(f"\n  [{cat.upper()}] - {desc}")
        for s in skills:
            print(f"    - {s['id']:<28} {s.get('description', '')[:65]}")

    held = [r for r in manifest.get("resources", []) if not r.get("installable")]
    if held:
        print("\n🔒 Held / Special-Review Resources (Excluded from defaults):")
        for h in held:
            status = h.get("status", "held")
            reason = h.get("securityReview", {}).get("notes", h.get("description", ""))[:65]
            print(f"    ! {h['id']:<28} [{status}] {reason}")

    print("\nRun './scripts/essentials install <preset|skill> --target <dir>' to install.")
    return 0


# --------------------------------------------------------------------------- Command: Validate

def cmd_validate(args: argparse.Namespace) -> int:
    """Validate repository integrity, skill hashes, forbidden files, and schema."""
    manifest = load_manifest()
    errors: list[str] = []
    warnings: list[str] = []
    resources = manifest.get("resources", [])

    if manifest.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")

    ids = [r["id"] for r in resources]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"duplicate id: {dup}")

    library_dir = REPO_ROOT / "resources"

    for r in resources:
        rid = r["id"]
        review = r.get("securityReview", {})
        if review.get("status") not in REVIEW_STATUSES:
            errors.append(f"{rid}: securityReview.status must be one of {sorted(REVIEW_STATUSES)}")

        if not r.get("installable"):
            if r.get("path") and r.get("kind") == "skill":
                errors.append(f"{rid}: held skill must not declare a vendored path in the library")
            continue

        if r.get("status") != "vendored":
            errors.append(f"{rid}: installable entries must have status 'vendored'")

        rel_path = r.get("path")
        if not rel_path:
            errors.append(f"{rid}: missing path")
            continue

        skill_dir = library_dir / rel_path
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{rid}: {skill_md} is missing")
            continue

        # Frontmatter check
        text = skill_md.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        fields: dict[str, str] = {}
        if match:
            for line in match.group(1).splitlines():
                if ":" in line and not line.startswith((" ", "\t")):
                    k, v = line.split(":", 1)
                    fields[k.strip()] = v.strip().strip('"\'')

        if fields.get("name") != rid:
            errors.append(f"{rid}: frontmatter name '{fields.get('name')}' does not match id")
        if not fields.get("description"):
            errors.append(f"{rid}: frontmatter description is missing or empty")

        # Hash check
        expected_sha = r.get("skillMd", {}).get("sha256")
        actual_sha = sha256_file(skill_md)
        if expected_sha and actual_sha != expected_sha:
            errors.append(f"{rid}: SKILL.md SHA-256 hash mismatch! Tampering detected.")

        # Collection licenses
        col_rel = r.get("collection")
        if col_rel:
            col_dir = library_dir / "skills" / col_rel
            if not any(col_dir.glob("LICENSE*")):
                errors.append(f"{rid}: no LICENSE file in collection {col_rel}")
            if not (col_dir / "SOURCE.md").is_file():
                errors.append(f"{rid}: no SOURCE.md in collection {col_rel}")

        # Forbidden files
        for root, dirs, files in os.walk(skill_dir):
            for fname in files:
                if fname in FORBIDDEN_NAMES:
                    errors.append(f"{rid}: forbidden configuration file found: {Path(root, fname).relative_to(REPO_ROOT)}")
            for dname in dirs:
                if dname in FORBIDDEN_DIRS:
                    errors.append(f"{rid}: forbidden directory found: {Path(root, dname).relative_to(REPO_ROOT)}")
            for item in files + dirs:
                full_item = Path(root, item)
                if full_item.is_symlink():
                    errors.append(f"{rid}: illegal symlink inside library: {full_item.relative_to(REPO_ROOT)}")

    # Check presets
    known_skills = {r["id"] for r in resources if r.get("installable")}
    for pname, pdata in manifest.get("presets", {}).items():
        for sid in pdata.get("skills", []):
            if sid not in known_skills:
                errors.append(f"preset '{pname}' references unknown or held skill '{sid}'")

    for line in errors:
        print(f"ERROR   {line}")
    for line in warnings:
        print(f"WARNING {line}")

    presets_count = len(manifest.get("presets", {}))
    print(f"\nValidation Summary: {len(known_skills)} installable skills, {presets_count} presets, "
          f"{len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


# --------------------------------------------------------------------------- Command: Install

def cmd_install(args: argparse.Namespace) -> int:
    """Install a preset or individual skills into a target project."""
    manifest = load_manifest()
    installable = get_installable_resources(manifest)
    project = resolve_project_dir(args.target)

    # Determine requested skills
    requested_ids: list[str] = []
    if args.preset:
        for p in args.preset:
            if p not in manifest.get("presets", {}):
                raise CLIError(f"unknown preset '{p}'. Available: {', '.join(manifest.get('presets', {}).keys())}")
            requested_ids.extend(manifest["presets"][p]["skills"])

    if args.skills:
        requested_ids.extend(args.skills)

    # Also handle positional selector (could be a preset name or comma-separated skill list)
    if args.selector:
        for token in args.selector.split(","):
            token = token.strip()
            if not token:
                continue
            if token in manifest.get("presets", {}):
                requested_ids.extend(manifest["presets"][token]["skills"])
            else:
                requested_ids.append(token)

    if not requested_ids:
        raise CLIError("no skills or preset selected for installation. Specify a preset or --skills (see 'list')")

    # Deduplicate while preserving order
    unique_ids: list[str] = []
    for sid in requested_ids:
        if sid not in unique_ids:
            unique_ids.append(sid)

    # Check for invalid or held skills
    invalid = [sid for sid in unique_ids if sid not in installable]
    if invalid:
        raise CLIError(f"the following skills are unknown or not installable: {', '.join(invalid)}")

    # Resolve agent adapter
    agent_name = args.agent or "claude-code"
    adapter = get_adapter(agent_name)

    ledger = read_project_ledger(project)
    installs_record = ledger.get("installs", {})

    # Plan installations & detect conflicts
    plan: list[tuple[dict[str, Any], Path]] = []
    conflicts: list[str] = []
    skipped: list[str] = []

    for sid in unique_ids:
        resource = installable[sid]
        dest = adapter.get_destination_path(project, sid)

        # Check if already managed in ledger
        if sid in installs_record:
            rec = installs_record[sid]
            if rec.get("agent") == adapter.name and os.path.lexists(dest):
                skipped.append(f"{sid}: already installed for {adapter.name}")
                continue

        # Check for unmanaged file conflicts
        if os.path.lexists(dest):
            conflicts.append(f"{sid}: destination {dest.relative_to(project)} already exists and is not managed by Essentials")
            continue

        plan.append((resource, dest))

    if conflicts:
        print("Installation aborted due to conflicts (no files were modified):", file=sys.stderr)
        for c in conflicts:
            print(f"  ! {c}", file=sys.stderr)
        print("Remove or rename conflicting files, or select a different target directory.", file=sys.stderr)
        return 1

    mode = args.mode or ("copy" if adapter.name in ("cursor", "windsurf", "copilot") else "link")

    print(f"Target Project: {project}")
    print(f"Agent Adapter:  {adapter.name} ({adapter.description})")
    print(f"Install Mode:   {mode}")
    print("\nPlanned Changes:")
    for res, dest in plan:
        print(f"  + [{mode}] {res['id']:<28} -> {dest.relative_to(project)}")
    for s in skipped:
        print(f"  . {s}")

    if not plan:
        print("\nNo new skills to install.")
        return 0

    if args.dry_run:
        print("\nDry run: no files changed.")
        return 0

    if not args.yes:
        if not ask_confirmation("\nProceed with installation? [y/N]: "):
            print("Cancelled. No changes made.")
            return 1

    # Execute installation
    library_dir = REPO_ROOT / "resources"
    installed_count = 0
    failures: list[str] = []

    for res, dest in plan:
        sid = res["id"]
        source_dir = library_dir / res["path"]
        try:
            _, record = adapter.install(project, res, source_dir, mode=mode)
            record["installedAt"] = now_iso()
            installs_record[sid] = record
            installed_count += 1
        except Exception as exc:
            failures.append(f"{sid}: {exc}")

    write_project_ledger(project, ledger)

    print(f"\nInstalled {installed_count} of {len(plan)} skill(s) into {project}.")
    if failures:
        print("Failures encountered:", file=sys.stderr)
        for f in failures:
            print(f"  ! {f}", file=sys.stderr)
        return 1

    print(f"Installation ledger updated at: {project / LEDGER_NAME}")
    return 0


# --------------------------------------------------------------------------- Command: Status

def cmd_status(args: argparse.Namespace) -> int:
    """Inspect the current installation status and ledger integrity of a project."""
    project = resolve_project_dir(args.target)
    ledger = read_project_ledger(project)
    installs = ledger.get("installs", {})

    print(f"Status for: {project}")
    if not installs:
        print("  No Essentials skills currently installed.")
        return 0

    print(f"  Total Managed Skills: {len(installs)}")
    print("\n  Skill Breakdown:")
    for sid, rec in sorted(installs.items()):
        agent_name = rec.get("agent", "claude-code")
        mode = rec.get("mode", "unknown")
        try:
            adapter = get_adapter(agent_name)
            valid, reason = adapter.verify(project, sid, rec)
            status_label = "OK" if valid else f"TAMPERED/MISSING ({reason})"
        except Exception as exc:
            status_label = f"ERROR ({exc})"
        dest = rec.get("destination", sid)
        print(f"    • {sid:<26} [agent: {agent_name:<11} | mode: {mode:<4}] -> {dest} [{status_label}]")

    return 0


# --------------------------------------------------------------------------- Command: Uninstall

def cmd_uninstall(args: argparse.Namespace) -> int:
    """Safely uninstall skills managed by Essentials, protecting user modifications."""
    project = resolve_project_dir(args.target)
    ledger = read_project_ledger(project)
    installs = ledger.get("installs", {})

    if not installs:
        print(f"Nothing to uninstall: no Essentials records found for {project}.")
        return 0

    # Determine skills to uninstall
    target_skills = args.skills or []
    if args.selector:
        target_skills.extend([s.strip() for s in args.selector.split(",") if s.strip()])

    removable: list[str] = []
    kept: list[str] = []

    skills_to_evaluate = target_skills if target_skills else list(installs.keys())

    for sid in skills_to_evaluate:
        if sid not in installs:
            kept.append(f"{sid}: not recorded in ledger, skipped")
            continue
        rec = installs[sid]
        agent_name = rec.get("agent", "claude-code")
        adapter = get_adapter(agent_name)
        dest = project / rec.get("destination", sid)

        if not os.path.lexists(dest):
            removable.append(sid)
        elif rec.get("mode") == "link":
            if dest.is_symlink() and os.readlink(dest) == rec.get("source"):
                removable.append(sid)
            else:
                kept.append(f"{sid}: symlink was altered or replaced; left in place")
        else:
            # File or directory copy: check hash
            if dest.is_file():
                if sha256_file(dest) == rec.get("sha256"):
                    removable.append(sid)
                else:
                    kept.append(f"{sid}: file copy was modified by user; left in place")
            elif dest.is_dir() and not dest.is_symlink():
                if tree_digest(dest) == rec.get("treeSha256"):
                    removable.append(sid)
                else:
                    kept.append(f"{sid}: directory copy was modified by user; left in place")
            else:
                kept.append(f"{sid}: unknown file type; left in place")

    print(f"Uninstall Plan for {project}:")
    for sid in removable:
        print(f"  - remove {sid}")
    for k in kept:
        print(f"  . {k}")

    if not removable:
        print("\nNothing safe to remove.")
        return 0

    if args.dry_run:
        print("\nDry run: no files changed.")
        return 0

    if not args.yes:
        if not ask_confirmation("\nProceed with uninstallation? [y/N]: "):
            print("Cancelled. No changes made.")
            return 1

    removed_count = 0
    for sid in removable:
        rec = installs[sid]
        dest = project / rec.get("destination", sid)
        if os.path.lexists(dest):
            if dest.is_symlink() or dest.is_file():
                dest.unlink()
            elif dest.is_dir():
                shutil.rmtree(dest)
        del installs[sid]
        removed_count += 1

    write_project_ledger(project, ledger)
    print(f"\nRemoved {removed_count} install(s). {len(installs)} record(s) remaining.")
    return 0


# --------------------------------------------------------------------------- Command: Search

def cmd_search(args: argparse.Namespace) -> int:
    """Search for skills across id, description, use cases, and categories."""
    manifest = load_manifest()
    query = args.query.strip().lower()
    cat_filter = getattr(args, "category", None)
    if cat_filter:
        cat_filter = cat_filter.strip().lower()

    matches = []
    for r in manifest.get("resources", []):
        if cat_filter and r.get("category", "").lower() != cat_filter:
            continue
        text_corpus = f"{r.get('id', '')} {r.get('description', '')} {r.get('useCases', '')} {r.get('category', '')}".lower()
        if query in text_corpus:
            matches.append(r)

    if getattr(args, "json", False):
        print(json.dumps(matches, indent=2))
        return 0

    print(f"Search results for '{args.query}' ({len(matches)} match(es)):\n")
    if not matches:
        print("  No skills matched your search criteria.")
        return 0

    for r in matches:
        status_tag = "installable" if r.get("installable") else f"[{r.get('status', 'held')}]"
        print(f"  • {r['id']:<28} [{r.get('category', 'general'):<12}] ({status_tag})")
        print(f"    {r.get('description', '')[:75]}")
        if r.get("useCases"):
            print(f"    Use cases: {r['useCases'][:75]}")
        print()
    return 0


# --------------------------------------------------------------------------- Command: Inspect

def cmd_inspect(args: argparse.Namespace) -> int:
    """Inspect complete metadata and provenance for a specific skill or preset."""
    manifest = load_manifest()
    target_id = args.skill_id.strip()

    # Check if target is a preset
    if target_id in manifest.get("presets", {}):
        pdata = manifest["presets"][target_id]
        if getattr(args, "json", False):
            print(json.dumps({target_id: pdata}, indent=2))
            return 0
        print("=" * 65)
        print(f" PRESET: {target_id}")
        print("=" * 65)
        print(f"Description: {pdata.get('description', '')}")
        print(f"Included Skills ({len(pdata.get('skills', []))}):")
        for sid in pdata.get("skills", []):
            print(f"  • {sid}")
        return 0

    # Search for matching resource
    matched = None
    for r in manifest.get("resources", []):
        if r.get("id") == target_id:
            matched = r
            break

    if not matched:
        raise CLIError(f"skill or preset '{target_id}' not found in manifest")

    if getattr(args, "json", False):
        print(json.dumps(matched, indent=2))
        return 0

    print("=" * 65)
    print(f" SKILL: {matched['id']}")
    print("=" * 65)
    print(f"  Category:        {matched.get('category', 'general')}")
    print(f"  Kind:            {matched.get('kind', 'skill')}")
    print(f"  Status:          {matched.get('status', 'unknown')}")
    print(f"  Installable:     {'Yes' if matched.get('installable') else 'No'}")
    print(f"  Safe for Default:{'Yes' if matched.get('safeForDefault') else 'No'}")
    print(f"  License:         {matched.get('license', 'Unspecified')}")
    print(f"  Description:     {matched.get('description', '')}")
    if matched.get("useCases"):
        print(f"  Use Cases:       {matched['useCases']}")

    src = matched.get("source", {})
    if src:
        print(f"\n  Upstream Source:")
        print(f"    Repository:    {src.get('repo', 'None')}")
        print(f"    Commit:        {src.get('commit', 'None')} ({src.get('commitDate', '')})")
        print(f"    Upstream Path: {src.get('upstreamPath', '')}")

    sec = matched.get("securityReview", {})
    if sec:
        print(f"\n  Security Review:")
        print(f"    Status:        {sec.get('status', 'unreviewed')}")
        print(f"    Date:          {sec.get('date', 'None')}")
        print(f"    Notes:         {sec.get('notes', 'None')}")

    agents = matched.get("supportedAgents", [])
    if agents:
        print(f"\n  Supported Agents: {', '.join(agents)}")
    return 0


# --------------------------------------------------------------------------- Command: Sync

def cmd_sync(args: argparse.Namespace) -> int:
    """Synchronize installed skills in a project to match canonical library versions."""
    manifest = load_manifest()
    installable = get_installable_resources(manifest)
    project = resolve_project_dir(args.target)
    ledger = read_project_ledger(project)
    installs = ledger.get("installs", {})

    if not installs:
        # If no installs, check if a preset was provided to initialize
        preset_name = getattr(args, "preset", None) or getattr(args, "selector", None)
        if preset_name and preset_name in manifest.get("presets", {}):
            print(f"No existing installs found. Initializing project with preset '{preset_name}'...")
            args.skills = manifest["presets"][preset_name]["skills"]
            args.preset = None
            args.selector = None
            return cmd_install(args)
        print(f"Nothing to sync: no installed skills recorded in {project}.")
        print("To install skills or a preset, use 'install' (e.g. './scripts/essentials install portfolio --target <dir>').")
        return 0

    library_dir = REPO_ROOT / "resources"
    updated_count = 0
    up_to_date_count = 0
    skipped_modified = 0

    print(f"Synchronizing installed skills for: {project}")
    for sid, rec in list(installs.items()):
        if sid not in installable:
            print(f"  ! {sid}: no longer in installable manifest; kept as-is")
            continue

        res = installable[sid]
        agent_name = rec.get("agent", "claude-code")
        adapter = get_adapter(agent_name)
        dest = project / rec.get("destination", sid)
        source_dir = library_dir / res["path"]

        # Check if destination exists
        if not os.path.lexists(dest):
            print(f"  + {sid}: missing from disk, restoring...")
            _, new_rec = adapter.install(project, res, source_dir, mode=rec.get("mode", "link"))
            new_rec["installedAt"] = now_iso()
            installs[sid] = new_rec
            updated_count += 1
            continue

        # For link mode: verify link target
        if rec.get("mode") == "link":
            if dest.is_symlink() and os.readlink(dest) == str(source_dir.resolve()):
                up_to_date_count += 1
            else:
                print(f"  ↻ {sid}: updating symlink target...")
                dest.unlink()
                os.symlink(source_dir.resolve(), dest, target_is_directory=True)
                rec["source"] = str(source_dir.resolve())
                rec["installedAt"] = now_iso()
                updated_count += 1
        else:
            # For copy mode: verify hash
            current_sha = sha256_file(dest) if dest.is_file() else tree_digest(dest)
            canonical_sha = res.get("skillMd", {}).get("sha256")
            if rec.get("sha256") and current_sha != rec["sha256"]:
                print(f"  . {sid}: local modifications detected; preserved without overwriting")
                skipped_modified += 1
            elif rec.get("sha256") == canonical_sha:
                up_to_date_count += 1
            else:
                print(f"  ↻ {sid}: updating copy to latest canonical version...")
                if dest.is_file():
                    dest.unlink()
                elif dest.is_dir():
                    shutil.rmtree(dest)
                _, new_rec = adapter.install(project, res, source_dir, mode="copy")
                new_rec["installedAt"] = now_iso()
                installs[sid] = new_rec
                updated_count += 1

    write_project_ledger(project, ledger)
    print(f"\nSync complete: {updated_count} updated, {up_to_date_count} up-to-date, {skipped_modified} user-modified kept.")
    return 0


# --------------------------------------------------------------------------- CLI Parser Builder

def build_cli_parser() -> argparse.ArgumentParser:
    """Build top-level ArgumentParser for Essentials CLI."""
    parser = argparse.ArgumentParser(
        prog="essentials",
        description="Universal AI Developer Toolkit: cross-agent skills, configs, and templates.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # list
    p_list = subparsers.add_parser("list", help="List available skills, presets, and supported agents")
    p_list.add_argument("--json", action="store_true", help="Output in machine-readable JSON format")
    p_list.set_defaults(func=cmd_list)

    # search
    p_search = subparsers.add_parser("search", help="Search available skills by keyword or category")
    p_search.add_argument("query", help="Search keyword")
    p_search.add_argument("--category", "-c", help="Filter by category (e.g. robotics-ml, audio, engineering)")
    p_search.add_argument("--json", action="store_true", help="Output in machine-readable JSON format")
    p_search.set_defaults(func=cmd_search)

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspect provenance, license, and security details of a skill or preset")
    p_inspect.add_argument("skill_id", help="Skill ID or preset name")
    p_inspect.add_argument("--json", action="store_true", help="Output in machine-readable JSON format")
    p_inspect.set_defaults(func=cmd_inspect)

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate skill manifests, hashes, and security rules")
    p_validate.set_defaults(func=cmd_validate)

    # install
    p_install = subparsers.add_parser("install", help="Install skills or a preset into a target project")
    p_install.add_argument("selector", nargs="?", help="Preset name (e.g. 'portfolio') or skill id(s)")
    p_install.add_argument("--target", "-t", required=True, help="Target project directory path")
    p_install.add_argument("--preset", "-p", action="append", help="Preset name to install (repeatable)")
    p_install.add_argument(
        "--skills", "-s",
        type=lambda s: [x.strip() for x in s.split(",") if x.strip()],
        action="append",
        help="Comma-separated skill IDs to install (repeatable)",
    )
    p_install.add_argument("--agent", "-a", default="claude-code", help="Target agent (e.g. claude, cursor, codex, gemini, windsurf, copilot)")
    p_install.add_argument("--mode", "-m", choices=["link", "copy"], help="Install mode: symlink or copy")
    p_install.add_argument("--dry-run", action="store_true", help="Preview planned changes without writing to disk")
    p_install.add_argument("--yes", "-y", action="store_true", help="Skip interactive confirmation prompts")
    p_install.set_defaults(func=cmd_install)

    # sync
    p_sync = subparsers.add_parser("sync", help="Synchronize installed project skills against canonical library")
    p_sync.add_argument("selector", nargs="?", help="Optional preset name to initialize if uninstalled")
    p_sync.add_argument("--target", "-t", required=True, help="Target project directory path")
    p_sync.add_argument("--preset", "-p", help="Optional preset name")
    p_sync.add_argument("--agent", "-a", default="claude-code", help="Target agent format")
    p_sync.add_argument("--mode", "-m", choices=["link", "copy"], help="Install mode")
    p_sync.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    p_sync.set_defaults(func=cmd_sync)

    # status
    p_status = subparsers.add_parser("status", help="Inspect installation status and verify file integrity")
    p_status.add_argument("--target", "-t", required=True, help="Target project directory path")
    p_status.set_defaults(func=cmd_status)

    # uninstall
    p_uninstall = subparsers.add_parser("uninstall", help="Safely remove Essentials-managed skills from a project")
    p_uninstall.add_argument("selector", nargs="?", help="Optional specific skill ID(s) to uninstall")
    p_uninstall.add_argument("--target", "-t", required=True, help="Target project directory path")
    p_uninstall.add_argument(
        "--skills", "-s",
        type=lambda s: [x.strip() for x in s.split(",") if x.strip()],
        action="append",
        help="Comma-separated skill IDs to uninstall (repeatable)",
    )
    p_uninstall.add_argument("--dry-run", action="store_true", help="Preview uninstall without modifying files")
    p_uninstall.add_argument("--yes", "-y", action="store_true", help="Skip interactive confirmation prompts")
    p_uninstall.set_defaults(func=cmd_uninstall)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for Essentials CLI."""
    parser = build_cli_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    # Flatten skills arguments if present
    if hasattr(args, "skills") and args.skills:
        args.skills = [s for group in args.skills for s in group]

    try:
        return args.func(args)
    except CLIError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())

