"""Global skill management for Essentials.

Manages system-wide personal skill installations shared across
OpenCode, Claude Code, and VS Code with GitHub Copilot on Linux.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from adapters.base import sha256_file, tree_digest


class GlobalManagerError(Exception):
    """Raised for global skill manager errors."""
    pass


# --------------------------------------------------------------------------- Configuration & Paths

def find_repo_root() -> Path:
    """Detect Essentials repository root dynamically.

    Precedence:
    1. Current working directory (if it contains resources/resources.json)
    2. ESSENTIALS_REPO environment variable
    3. Directory containing this script (fallback)
    """
    cwd = Path.cwd().resolve()
    if (cwd / "resources" / "resources.json").is_file() and (cwd / "resources" / "skills").is_dir():
        return cwd

    env_repo = os.environ.get("ESSENTIALS_REPO")
    if env_repo:
        p = Path(env_repo).expanduser().resolve()
        if (p / "resources" / "resources.json").is_file():
            return p

    script_repo = Path(__file__).resolve().parent.parent
    if (script_repo / "resources" / "resources.json").is_file():
        return script_repo

    raise GlobalManagerError("Cannot locate Essentials repository root. Run from repository or set ESSENTIALS_REPO.")


def get_global_ledger_path() -> Path:
    """Return path to dedicated global installation ledger.

    Precedence:
    1. ESSENTIALS_GLOBAL_LEDGER environment variable (for testing & custom locations)
    2. $XDG_CONFIG_HOME/essentials/global-ledger.json
    3. ~/.config/essentials/global-ledger.json
    """
    env_ledger = os.environ.get("ESSENTIALS_GLOBAL_LEDGER")
    if env_ledger:
        return Path(env_ledger).expanduser().resolve()

    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        base = Path(xdg).expanduser().resolve()
    else:
        base = Path.home() / ".config"

    return base / "essentials" / "global-ledger.json"


def get_target_directory(target_key: str) -> Path:
    """Resolve the base skills directory for a given agent target."""
    if target_key == "claude-code":
        env = os.environ.get("CLAUDE_SKILLS_DIR")
        return Path(env).expanduser().resolve() if env else (Path.home() / ".claude" / "skills")
    elif target_key == "shared-agents":
        env = os.environ.get("AGENTS_SKILLS_DIR")
        return Path(env).expanduser().resolve() if env else (Path.home() / ".agents" / "skills")
    elif target_key == "opencode":
        env = os.environ.get("OPENCODE_SKILLS_DIR")
        return Path(env).expanduser().resolve() if env else (Path.home() / ".config" / "opencode" / "skills")
    elif target_key == "copilot":
        env = os.environ.get("COPILOT_SKILLS_DIR")
        return Path(env).expanduser().resolve() if env else (Path.home() / ".copilot" / "skills")
    else:
        raise GlobalManagerError(f"unknown target key '{target_key}'")


TARGET_METADATA = {
    "claude-code": {
        "name": "claude-code",
        "display": "Claude Code (~/.claude/skills)",
        "description": "Claude Code personal agent skills",
    },
    "shared-agents": {
        "name": "shared-agents",
        "display": "Shared Agent Skills (~/.agents/skills)",
        "description": "Standard Agent Skills open format (OpenCode, VS Code Copilot, Gemini CLI)",
    },
    "opencode": {
        "name": "opencode",
        "display": "OpenCode Dedicated (~/.config/opencode/skills)",
        "description": "OpenCode dedicated XDG skills directory",
    },
    "copilot": {
        "name": "copilot",
        "display": "GitHub Copilot Dedicated (~/.copilot/skills)",
        "description": "GitHub Copilot dedicated personal skills directory",
    },
}


def resolve_active_targets(
    strategy: str = "shared",
    selected_agents: list[str] | None = None,
) -> dict[str, Path]:
    """Resolve active target agent keys and their corresponding disk directories."""
    if selected_agents:
        # User specified specific agent keys or aliases
        targets: dict[str, Path] = {}
        for item in selected_agents:
            cleaned = item.strip().lower()
            if cleaned in ("claude", "claude-code", "claudecode"):
                targets["claude-code"] = get_target_directory("claude-code")
            elif cleaned in ("shared", "agents", "shared-agents", "universal"):
                targets["shared-agents"] = get_target_directory("shared-agents")
            elif cleaned in ("opencode", "open-code"):
                if strategy == "shared":
                    targets["shared-agents"] = get_target_directory("shared-agents")
                else:
                    targets["opencode"] = get_target_directory("opencode")
            elif cleaned in ("copilot", "github-copilot", "vscode-copilot"):
                if strategy == "shared":
                    targets["shared-agents"] = get_target_directory("shared-agents")
                else:
                    targets["copilot"] = get_target_directory("copilot")
            elif cleaned == "all":
                return {
                    "claude-code": get_target_directory("claude-code"),
                    "shared-agents": get_target_directory("shared-agents"),
                    "opencode": get_target_directory("opencode"),
                    "copilot": get_target_directory("copilot"),
                }
            else:
                raise GlobalManagerError(
                    f"Unknown agent '{cleaned}'. Allowed: claude, opencode, copilot, shared, all"
                )
        return targets

    if strategy == "shared":
        # Shared Agent Skills convention covers OpenCode and VS Code Copilot, plus Claude Code
        return {
            "claude-code": get_target_directory("claude-code"),
            "shared-agents": get_target_directory("shared-agents"),
        }
    elif strategy == "dedicated":
        return {
            "claude-code": get_target_directory("claude-code"),
            "opencode": get_target_directory("opencode"),
            "copilot": get_target_directory("copilot"),
        }
    elif strategy == "all":
        return {
            "claude-code": get_target_directory("claude-code"),
            "shared-agents": get_target_directory("shared-agents"),
            "opencode": get_target_directory("opencode"),
            "copilot": get_target_directory("copilot"),
        }
    else:
        raise GlobalManagerError(f"Invalid strategy '{strategy}'. Allowed: shared, dedicated, all")


# --------------------------------------------------------------------------- Ledger Read / Write

def read_global_ledger(ledger_path: Path | None = None) -> dict[str, Any]:
    """Read global installation ledger, initializing standard schema if absent."""
    path = ledger_path or get_global_ledger_path()
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data.setdefault("version", 1)
            data.setdefault("targets", {})
            return data
        except Exception as exc:
            raise GlobalManagerError(
                f"Corrupt global ledger file {path}: {exc}. To reset, backup or remove this file."
            ) from exc

    return {
        "version": 1,
        "repoRoot": str(find_repo_root()),
        "updatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "targets": {},
    }


def write_global_ledger(ledger: dict[str, Any], ledger_path: Path | None = None) -> None:
    """Atomically write global installation ledger to disk."""
    path = ledger_path or get_global_ledger_path()

    # If completely empty across all targets, remove ledger file cleanly
    has_installs = any(
        target_info.get("installs")
        for target_info in ledger.get("targets", {}).values()
    )
    if not has_installs:
        if path.is_file():
            path.unlink()
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    ledger["updatedAt"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


# --------------------------------------------------------------------------- Core Global Operations

def setup_global(
    manifest: dict[str, Any],
    requested_skills: list[str],
    strategy: str = "shared",
    agents: list[str] | None = None,
    mode: str = "link",
    dry_run: bool = False,
    yes: bool = False,
    ledger_path: Path | None = None,
) -> int:
    """Install skills globally into target agent directories with symlinks or safe copies."""
    repo_root = find_repo_root()
    library_dir = repo_root / "resources"
    installable = {
        r["id"]: r
        for r in manifest.get("resources", [])
        if r.get("installable")
    }

    if not requested_skills:
        raise GlobalManagerError("No skills specified for global installation.")

    # Validate that all requested skills exist in canonical library
    for sid in requested_skills:
        if sid not in installable:
            raise GlobalManagerError(f"Unknown or non-installable skill '{sid}'.")

    targets = resolve_active_targets(strategy=strategy, selected_agents=agents)
    ledger = read_global_ledger(ledger_path)
    ledger_targets = ledger.setdefault("targets", {})

    # Pre-flight Conflict & Safety Checks
    conflicts: list[str] = []
    actions: list[dict[str, Any]] = []

    for t_key, t_dir in targets.items():
        t_installs = ledger_targets.setdefault(t_key, {
            "path": str(t_dir),
            "installs": {},
        }).setdefault("installs", {})

        for sid in requested_skills:
            res = installable[sid]
            source_dir = library_dir / res["path"]
            dest = t_dir / sid

            if not source_dir.is_dir():
                conflicts.append(f"Canonical source missing for skill '{sid}' at {source_dir}")
                continue

            # Check if destination exists
            if os.path.lexists(dest):
                if sid not in t_installs:
                    # Unmanaged skill or file exists! NEVER overwrite!
                    conflicts.append(
                        f"Unmanaged skill or directory already exists at {dest}. "
                        f"Essentials will never overwrite unmanaged user skills."
                    )
                    continue
                else:
                    # Managed installation exists: check state
                    existing_rec = t_installs[sid]
                    if existing_rec.get("mode") == "link":
                        if dest.is_symlink() and os.readlink(dest) == str(source_dir.resolve()):
                            # Already up to date
                            actions.append({
                                "target": t_key,
                                "skill": sid,
                                "dest": dest,
                                "source": source_dir.resolve(),
                                "action": "up-to-date",
                            })
                            continue
                        elif dest.is_symlink():
                            actions.append({
                                "target": t_key,
                                "skill": sid,
                                "dest": dest,
                                "source": source_dir.resolve(),
                                "action": "update-link",
                            })
                            continue
                        else:
                            conflicts.append(
                                f"Expected symlink at {dest} but found regular directory."
                            )
                            continue
                    else:
                        # Copy mode
                        actions.append({
                            "target": t_key,
                            "skill": sid,
                            "dest": dest,
                            "source": source_dir.resolve(),
                            "action": "update-copy",
                        })
                        continue

            actions.append({
                "target": t_key,
                "skill": sid,
                "dest": dest,
                "source": source_dir.resolve(),
                "action": "create",
            })

    if conflicts:
        print("ERROR: Safety pre-flight check failed with conflicts:\n", file=sys.stderr)
        for c in conflicts:
            print(f"  • {c}", file=sys.stderr)
        print("\nNo files or ledgers were modified.", file=sys.stderr)
        return 1

    # Report Plan
    print("=" * 72)
    print(" ESSENTIALS: System-Wide Global Skill Setup")
    print("=" * 72)
    print(f"Repository Root:   {repo_root}")
    print(f"Installation Mode: {mode.upper()} ({'canonical symlinks' if mode == 'link' else 'safe copies'})")
    print(f"Strategy:          {strategy}")
    print(f"Target Agents:     {', '.join(targets.keys())}")
    print(f"Global Ledger:     {ledger_path or get_global_ledger_path()}")
    print("\nPlanned Actions:")

    for act in actions:
        t_disp = TARGET_METADATA.get(act["target"], {}).get("display", act["target"])
        status_sym = "+" if act["action"] == "create" else ("↻" if "update" in act["action"] else "=")
        print(f"  {status_sym} [{act['target']:<14}] {act['skill']:<26} -> {act['action']}")

    if dry_run:
        print("\n[DRY RUN]: Preview mode active. Zero files or ledger entries were modified.")
        return 0

    # Execution Phase
    installed_count = 0
    updated_count = 0
    now_ts = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    for act in actions:
        if act["action"] == "up-to-date":
            continue

        t_key = act["target"]
        t_dir = targets[t_key]
        sid = act["skill"]
        source_dir = act["source"]
        dest = act["dest"]
        t_installs = ledger_targets[t_key]["installs"]

        dest.parent.mkdir(parents=True, exist_ok=True)

        if os.path.lexists(dest):
            if dest.is_symlink() or dest.is_file():
                dest.unlink()
            elif dest.is_dir():
                shutil.rmtree(dest)

        skill_md = source_dir / "SKILL.md"
        sha = sha256_file(skill_md) if skill_md.is_file() else ""
        tree_sha = tree_digest(source_dir) if source_dir.is_dir() else ""

        if mode == "link":
            os.symlink(source_dir, dest, target_is_directory=True)
        else:
            shutil.copytree(source_dir, dest, symlinks=False)

        t_installs[sid] = {
            "mode": mode,
            "source": str(source_dir),
            "destination": str(dest),
            "sha256": sha,
            "treeSha256": tree_sha,
            "installedAt": now_ts,
        }

        if act["action"] == "create":
            installed_count += 1
        else:
            updated_count += 1

    ledger["repoRoot"] = str(repo_root)
    write_global_ledger(ledger, ledger_path)

    print(f"\nGlobal setup completed successfully!")
    print(f"  • {installed_count} skill(s) installed")
    print(f"  • {updated_count} skill(s) updated")
    print(f"  • {len(actions) - installed_count - updated_count} skill(s) already up-to-date")
    print("\nSkills are now instantly active system-wide across all configured agent tools.")
    return 0


def global_status(
    manifest: dict[str, Any] | None = None,
    as_json: bool = False,
    ledger_path: Path | None = None,
) -> int:
    """Inspect global installation ledger and detect unmanaged, broken, or modified skills."""
    ledger = read_global_ledger(ledger_path)
    report: dict[str, Any] = {
        "ledgerPath": str(ledger_path or get_global_ledger_path()),
        "repoRoot": ledger.get("repoRoot"),
        "updatedAt": ledger.get("updatedAt"),
        "targets": {},
    }

    # Inspect all supported targets whether in ledger or not
    all_targets = {
        "claude-code": get_target_directory("claude-code"),
        "shared-agents": get_target_directory("shared-agents"),
        "opencode": get_target_directory("opencode"),
        "copilot": get_target_directory("copilot"),
    }

    for t_key, t_dir in all_targets.items():
        t_data = ledger.get("targets", {}).get(t_key, {})
        installs = t_data.get("installs", {})
        managed_report: dict[str, Any] = {}
        unmanaged_skills: list[str] = []

        # Check managed skills
        for sid, rec in installs.items():
            dest = Path(rec.get("destination", t_dir / sid))
            status_item: dict[str, Any] = {
                "mode": rec.get("mode", "link"),
                "source": rec.get("source"),
                "destination": str(dest),
                "installedAt": rec.get("installedAt"),
            }

            if not os.path.lexists(dest):
                status_item["status"] = "missing"
            elif rec.get("mode") == "link":
                if not dest.is_symlink():
                    status_item["status"] = "expected-symlink-found-dir"
                elif not os.path.exists(dest):
                    status_item["status"] = "broken-link"
                elif os.readlink(dest) != rec.get("source"):
                    status_item["status"] = "altered-symlink"
                else:
                    status_item["status"] = "healthy"
            else:
                # Copy mode
                if not dest.is_dir():
                    status_item["status"] = "missing-dir"
                else:
                    curr_tree = tree_digest(dest)
                    if rec.get("treeSha256") and curr_tree != rec["treeSha256"]:
                        status_item["status"] = "user-modified"
                    else:
                        status_item["status"] = "healthy"

            managed_report[sid] = status_item

        # Detect unmanaged items in directory
        if t_dir.is_dir():
            for item in sorted(t_dir.iterdir()):
                if item.name.startswith(".") or item.name in installs:
                    continue
                unmanaged_skills.append(item.name)

        report["targets"][t_key] = {
            "path": str(t_dir),
            "exists": t_dir.is_dir(),
            "managedCount": len(managed_report),
            "managed": managed_report,
            "unmanagedCount": len(unmanaged_skills),
            "unmanaged": unmanaged_skills,
        }

    if as_json:
        print(json.dumps(report, indent=2))
        return 0

    print("=" * 76)
    print(" ESSENTIALS: Global Skills Status")
    print("=" * 76)
    print(f"Ledger Location: {report['ledgerPath']}")
    print(f"Repository Root: {report['repoRoot'] or 'Not registered'}")
    print(f"Last Updated:    {report['updatedAt'] or 'Never'}\n")

    for t_key, t_info in report["targets"].items():
        meta = TARGET_METADATA.get(t_key, {})
        disp_name = meta.get("display", t_key)
        print(f"📂 Target: {disp_name}")
        print(f"   Directory: {t_info['path']} ({'Exists' if t_info['exists'] else 'Not created'})")
        print(f"   Managed Skills ({t_info['managedCount']}):")

        if not t_info["managed"]:
            print("     (None recorded in global ledger)")
        else:
            for sid, sdata in t_info["managed"].items():
                st = sdata["status"]
                badge = "✓" if st == "healthy" else "!"
                mode_str = f"[{sdata['mode']}]"
                print(f"     {badge} {sid:<24} {mode_str:<6} {st}")

        if t_info["unmanaged"]:
            print(f"   Unmanaged User Skills / Files ({t_info['unmanagedCount']}) - Preserved:")
            for um in t_info["unmanaged"]:
                print(f"     • {um:<24} [user-owned, will never be removed by Essentials]")
        print()

    return 0


def global_sync(
    manifest: dict[str, Any],
    dry_run: bool = False,
    yes: bool = False,
    ledger_path: Path | None = None,
) -> int:
    """Synchronize all globally installed skills to latest canonical library versions."""
    repo_root = find_repo_root()
    library_dir = repo_root / "resources"
    installable = {
        r["id"]: r
        for r in manifest.get("resources", [])
        if r.get("installable")
    }

    ledger = read_global_ledger(ledger_path)
    ledger_targets = ledger.get("targets", {})

    total_installs = sum(len(t.get("installs", {})) for t in ledger_targets.values())
    if total_installs == 0:
        print("Nothing to sync: no global skills recorded in ledger.")
        print("Run 'essentials setup-global <preset|skill>' to install global skills.")
        return 0

    print("=" * 72)
    print(" ESSENTIALS: Synchronizing Global Skills")
    print("=" * 72)
    print(f"Repository Root: {repo_root}")
    print(f"Global Ledger:   {ledger_path or get_global_ledger_path()}\n")

    repaired_count = 0
    updated_count = 0
    up_to_date_count = 0
    skipped_modified = 0
    now_ts = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    for t_key, t_data in ledger_targets.items():
        installs = t_data.get("installs", {})
        t_dir = Path(t_data.get("path", get_target_directory(t_key)))

        for sid, rec in list(installs.items()):
            if sid not in installable:
                print(f"  ! [{t_key}] {sid}: not in canonical manifest; kept as-is")
                continue

            res = installable[sid]
            source_dir = (library_dir / res["path"]).resolve()
            dest = Path(rec.get("destination", t_dir / sid))

            if not os.path.lexists(dest):
                print(f"  + [{t_key}] {sid}: missing on disk; restoring symlink...")
                if not dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    os.symlink(source_dir, dest, target_is_directory=True)
                    rec["source"] = str(source_dir)
                    rec["installedAt"] = now_ts
                repaired_count += 1
                continue

            if rec.get("mode") == "link":
                if dest.is_symlink() and os.readlink(dest) == str(source_dir):
                    up_to_date_count += 1
                else:
                    print(f"  ↻ [{t_key}] {sid}: updating symlink target...")
                    if not dry_run:
                        dest.unlink()
                        os.symlink(source_dir, dest, target_is_directory=True)
                        rec["source"] = str(source_dir)
                        rec["installedAt"] = now_ts
                    updated_count += 1
            else:
                # Copy mode
                curr_tree = tree_digest(dest)
                if rec.get("treeSha256") and curr_tree != rec["treeSha256"]:
                    print(f"  . [{t_key}] {sid}: local modifications detected; preserved without overwriting")
                    skipped_modified += 1
                else:
                    canonical_sha = res.get("skillMd", {}).get("sha256")
                    if rec.get("sha256") == canonical_sha:
                        up_to_date_count += 1
                    else:
                        print(f"  ↻ [{t_key}] {sid}: updating copy to latest canonical version...")
                        if not dry_run:
                            shutil.rmtree(dest)
                            shutil.copytree(source_dir, dest, symlinks=False)
                            rec["sha256"] = canonical_sha
                            rec["treeSha256"] = tree_digest(dest)
                            rec["installedAt"] = now_ts
                        updated_count += 1

    if not dry_run:
        write_global_ledger(ledger, ledger_path)

    print(f"\nSync complete:")
    print(f"  • {up_to_date_count} up-to-date")
    print(f"  • {repaired_count} restored")
    print(f"  • {updated_count} updated")
    print(f"  • {skipped_modified} user-modified copies preserved")
    return 0


def global_uninstall(
    manifest: dict[str, Any] | None = None,
    skill_ids: list[str] | None = None,
    uninstall_all: bool = False,
    dry_run: bool = False,
    yes: bool = False,
    ledger_path: Path | None = None,
) -> int:
    """Safely remove Essentials-managed skills from global agent directories."""
    ledger = read_global_ledger(ledger_path)
    ledger_targets = ledger.get("targets", {})

    total_installs = sum(len(t.get("installs", {})) for t in ledger_targets.values())
    if total_installs == 0:
        print("Nothing to uninstall: global ledger is empty.")
        return 0

    # Determine skills to target
    target_skill_ids: set[str] | None = None
    if not uninstall_all:
        if not skill_ids:
            raise GlobalManagerError("Specify skill ID(s) or pass --all to uninstall all global skills.")
        target_skill_ids = set(skill_ids)

    actions: list[dict[str, Any]] = []

    for t_key, t_data in ledger_targets.items():
        installs = t_data.get("installs", {})
        t_dir = Path(t_data.get("path", get_target_directory(t_key)))

        for sid, rec in list(installs.items()):
            if target_skill_ids is not None and sid not in target_skill_ids:
                continue

            dest = Path(rec.get("destination", t_dir / sid))
            if not os.path.lexists(dest):
                actions.append({
                    "target": t_key,
                    "skill": sid,
                    "dest": dest,
                    "action": "prune-missing-record",
                })
                continue

            if rec.get("mode") == "link":
                if dest.is_symlink():
                    expected = rec.get("source")
                    if expected and os.readlink(dest) != expected:
                        print(f"  ! [{t_key}] {sid}: symlink points to altered path {os.readlink(dest)}; kept")
                        continue
                    actions.append({
                        "target": t_key,
                        "skill": sid,
                        "dest": dest,
                        "action": "unlink",
                    })
                else:
                    print(f"  ! [{t_key}] {sid}: expected symlink but found normal directory; kept")
            else:
                # Copy mode: verify user modifications
                if dest.is_dir() and not dest.is_symlink():
                    curr_tree = tree_digest(dest)
                    if rec.get("treeSha256") and curr_tree != rec["treeSha256"]:
                        print(f"  ! [{t_key}] {sid}: directory was modified since installation; kept")
                        continue
                    actions.append({
                        "target": t_key,
                        "skill": sid,
                        "dest": dest,
                        "action": "remove-copy",
                    })

    if not actions:
        print("No matching managed skills eligible for removal.")
        return 0

    print("=" * 72)
    print(" ESSENTIALS: Global Skill Safe Uninstallation")
    print("=" * 72)
    print(f"Global Ledger: {ledger_path or get_global_ledger_path()}\n")
    print("Planned Removals:")
    for act in actions:
        print(f"  - [{act['target']:<14}] {act['skill']:<26} ({act['action']})")

    if dry_run:
        print("\n[DRY RUN]: Preview mode active. Zero files were removed.")
        return 0

    # Execute removal
    removed_count = 0
    for act in actions:
        t_key = act["target"]
        sid = act["skill"]
        dest = act["dest"]

        if act["action"] == "unlink":
            dest.unlink()
            removed_count += 1
        elif act["action"] == "remove-copy":
            shutil.rmtree(dest)
            removed_count += 1

        # Remove from ledger
        ledger_targets[t_key]["installs"].pop(sid, None)

    write_global_ledger(ledger, ledger_path)
    print(f"\nUninstall complete: safely removed {removed_count} skill installation(s).")
    print("All unmanaged user files and modified copies were preserved.")
    return 0
