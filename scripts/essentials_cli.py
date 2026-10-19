#!/usr/bin/env python3
"""Essentials CLI: Universal AI Developer Toolkit browser and validator.

Browse, search, inspect, and validate portable Agent Skills in skills/.
Standard library only. No installers or external dependencies required.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# Curated skill profiles (reference lists for convenient manual copying)
PRESETS = {
    "portfolio": {
        "description": "Creative portfolio development: Three.js 3D scenes, shaders, motion, audio, and visual design.",
        "skills": [
            "threejs/threejs-scene",
            "threejs/threejs-materials",
            "threejs/threejs-lighting",
            "threejs/threejs-shaders",
            "threejs/threejs-postprocessing",
            "threejs/threejs-animation",
            "threejs/threejs-geometry",
            "threejs/threejs-particles",
            "threejs/threejs-audio",
            "threejs/threejs-interaction",
            "threejs/threejs-performance",
            "threejs/threejs-accessibility",
            "threejs/threejs-html",
            "threejs/threejs-r3f",
            "threejs/threejs-web",
            "threejs/threejs-product-viewer",
            "threejs/threejs-assets",
            "threejs/threejs-debugging",
            "threejs/threejs-testing",
            "threejs/threejs-deployment",
            "design/frontend-design",
            "design/ui-ux-pro-max",
            "design/design",
            "design/design-md",
            "design/emil-design-eng",
            "design/animate",
            "design/animation-performance",
            "design/review-animations",
            "design/design-motion-principles",
            "design/apple-design",
            "audio/browser-audio",
        ],
    },
    "dashboard": {
        "description": "Data dashboards and administrative tools: information hierarchy, typography, and restrained motion.",
        "skills": [
            "design/frontend-design",
            "design/ui-ux-pro-max",
            "design/design",
            "design/design-md",
            "design/animation-performance",
            "design/review-animations",
        ],
    },
    "engineering": {
        "description": "Core software engineering suite: code review, TDD, Git hygiene, API design, security, and CI/CD.",
        "skills": [
            "engineering/code-review",
            "engineering/test-driven-development",
            "engineering/git-hygiene",
            "engineering/api-design",
            "engineering/security-audit",
            "engineering/ci-cd-workflow",
        ],
    },
    "python-dev": {
        "description": "Modern Python development: Pytest, clean architecture patterns, static typing, Asyncio, and pyproject packaging.",
        "skills": [
            "python/pytest-workflow",
            "python/python-patterns",
            "python/type-hints-modern",
            "python/asyncio-patterns",
            "python/packaging-pyproject",
            "engineering/code-review",
            "engineering/git-hygiene",
            "engineering/security-audit",
        ],
    },
    "robotics-ml": {
        "description": "Robotics, computer vision pipelines, dataset curation, model evaluation, and edge inference.",
        "skills": [
            "robotics-ml/computer-vision",
            "robotics-ml/model-evaluation",
            "robotics-ml/dataset-curation",
            "robotics-ml/edge-inference",
        ],
    },
    "full-stack": {
        "description": "Comprehensive full-stack engineering: frontend design, backend APIs, visual regression, security, and CI/CD.",
        "skills": [
            "engineering/code-review",
            "engineering/test-driven-development",
            "engineering/git-hygiene",
            "engineering/api-design",
            "engineering/security-audit",
            "design/frontend-design",
            "design/ui-ux-pro-max",
            "design/design-md",
            "testing/visual-regression",
            "engineering/ci-cd-workflow",
        ],
    },
}


class CLIError(Exception):
    """Raised for expected user-facing errors."""
    pass


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse YAML frontmatter from Markdown text."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        return {}, text
    raw_frontmatter, body = match.group(1), match.group(2)
    fields = {}
    for line in raw_frontmatter.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip().strip('"\'')
    return fields, body


def scan_skills() -> dict[str, dict[str, Any]]:
    """Scan skills/ directory and return map of skill_id -> metadata dict."""
    if not SKILLS_DIR.is_dir():
        return {}

    skills = {}
    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith((".", "_")):
            continue
        cat_name = cat_dir.name
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith((".", "_")):
                continue
            skill_id = skill_dir.name
            skill_md = skill_dir / "SKILL.md"
            description = ""
            if skill_md.is_file():
                try:
                    fields, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
                    description = fields.get("description", "")
                except Exception:
                    pass

            skills[skill_id] = {
                "id": skill_id,
                "category": cat_name,
                "path": f"skills/{cat_name}/{skill_id}",
                "fullPath": str(skill_dir),
                "description": description,
                "hasSkillMd": skill_md.is_file(),
            }
    return skills


# --------------------------------------------------------------------------- CLI Commands

def cmd_list(args: argparse.Namespace) -> int:
    """List available skills by category and curated profiles."""
    skills = scan_skills()

    if getattr(args, "json", False):
        grouped: dict[str, list[dict[str, Any]]] = {}
        for s in skills.values():
            grouped.setdefault(s["category"], []).append(s)
        print(json.dumps({
            "totalSkills": len(skills),
            "categories": grouped,
            "presets": PRESETS,
        }, indent=2))
        return 0

    print("=" * 78)
    print(" ESSENTIALS: Portable Agent Skills Library")
    print("=" * 78)
    print("\nCopy any skill folder into your agent's skills directory:")
    print("  cp -r skills/<category>/<skill-id> ~/.agents/skills/\n")

    print("📦 Curated Skill Profiles:")
    for pname, pdata in PRESETS.items():
        count = len(pdata["skills"])
        print(f"  • {pname:<14} {pdata['description']} ({count} skills)")

    grouped: dict[str, list[dict[str, Any]]] = {}
    for s in skills.values():
        grouped.setdefault(s["category"], []).append(s)

    print("\n🛠️ Available Skills by Category:")
    for cat in sorted(grouped.keys()):
        cat_skills = grouped[cat]
        print(f"\n  [{cat.upper()}] ({len(cat_skills)} skills)")
        for s in cat_skills:
            desc = (s["description"][:65] + "...") if len(s["description"]) > 65 else s["description"]
            print(f"    - {s['id']:<28} {desc}")

    print(f"\nTotal: {len(skills)} portable skills in skills/")
    print("To inspect any skill:  ./scripts/essentials inspect <skill-id>")
    print("To search by keyword:  ./scripts/essentials search <keyword>")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Search available skills by keyword or category."""
    skills = scan_skills()
    query = args.query.strip().lower()
    cat_filter = getattr(args, "category", None)
    if cat_filter:
        cat_filter = cat_filter.strip().lower()

    matches = []
    for s in skills.values():
        if cat_filter and s["category"].lower() != cat_filter:
            continue
        text_corpus = f"{s['id']} {s['category']} {s['description']}".lower()
        if query in text_corpus:
            matches.append(s)

    if getattr(args, "json", False):
        print(json.dumps(matches, indent=2))
        return 0

    if not matches:
        print(f"No skills found matching '{query}'.")
        return 1

    print(f"Search results for '{query}' ({len(matches)} match(es)):\n")
    for m in matches:
        desc = (m["description"][:60] + "...") if len(m["description"]) > 60 else m["description"]
        print(f"  • {m['id']:<28} [{m['category']:<12}]")
        print(f"    Path:    {m['path']}")
        print(f"    Summary: {desc}")
        print(f"    Install: cp -r {m['path']} ~/.agents/skills/\n")
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    """Inspect metadata, description, and manual-copy instructions for a skill or profile."""
    skills = scan_skills()
    target = args.skill_id.strip()

    # Check if target is a preset
    if target in PRESETS:
        pdata = PRESETS[target]
        if getattr(args, "json", False):
            print(json.dumps({target: pdata}, indent=2))
            return 0
        print("=" * 72)
        print(f" PROFILE: {target}")
        print("=" * 72)
        print(f"Description: {pdata['description']}")
        print(f"\nIncluded Skills ({len(pdata['skills'])}):")
        for sk in pdata["skills"]:
            print(f"  • {sk}")
        print(f"\nManual copy command:")
        print(f"  mkdir -p ~/.agents/skills")
        for sk in pdata["skills"]:
            print(f"  cp -r skills/{sk} ~/.agents/skills/")
        return 0

    # Search by skill ID
    matched = skills.get(target)
    if not matched:
        # Try case-insensitive or partial match
        for s in skills.values():
            if s["id"].lower() == target.lower():
                matched = s
                break

    if not matched:
        raise CLIError(f"skill or profile '{target}' not found. Run './scripts/essentials list' to view available skills.")

    if getattr(args, "json", False):
        print(json.dumps(matched, indent=2))
        return 0

    print("=" * 72)
    print(f" SKILL: {matched['id']}")
    print("=" * 72)
    print(f"  Category:        {matched['category']}")
    print(f"  Path:            {matched['path']}")
    print(f"  Description:     {matched['description']}")
    print(f"\n  Manual Copy Command:")
    print(f"    mkdir -p ~/.agents/skills")
    print(f"    cp -r {matched['path']} ~/.agents/skills/")
    print(f"\n  For Claude Code:")
    print(f"    mkdir -p ~/.claude/skills")
    print(f"    cp -r {matched['path']} ~/.claude/skills/")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate that every skill in skills/ has a valid SKILL.md with frontmatter."""
    if not SKILLS_DIR.is_dir():
        print(f"ERROR: {SKILLS_DIR} directory does not exist.", file=sys.stderr)
        return 1

    errors: list[str] = []
    skill_names: list[str] = []
    total_skills = 0

    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith((".", "_")):
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith((".", "_")):
                continue
            total_skills += 1
            sid = skill_dir.name
            skill_names.append(sid)

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                errors.append(f"{cat_dir.name}/{sid}: missing SKILL.md")
                continue

            try:
                content = skill_md.read_text(encoding="utf-8")
                fields, _ = parse_frontmatter(content)
                if not fields:
                    errors.append(f"{cat_dir.name}/{sid}: missing or invalid YAML frontmatter in SKILL.md")
                elif fields.get("name") != sid:
                    errors.append(f"{cat_dir.name}/{sid}: frontmatter name '{fields.get('name')}' != folder name '{sid}'")
                elif not fields.get("description"):
                    errors.append(f"{cat_dir.name}/{sid}: frontmatter description is missing or empty")
            except Exception as exc:
                errors.append(f"{cat_dir.name}/{sid}: error reading SKILL.md: {exc}")

    # Check for duplicate names
    dups = sorted({name for name in skill_names if skill_names.count(name) > 1})
    for dup in dups:
        errors.append(f"duplicate skill name found across categories: {dup}")

    for err in errors:
        print(f"ERROR   {err}")

    categories_count = len([d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith((".", "_"))])
    print(f"\nValidation Summary: {total_skills} skills across {categories_count} categories, "
          f"{len(errors)} error(s), 0 warning(s).")
    return 1 if errors else 0


# --------------------------------------------------------------------------- Parser & Main

def build_cli_parser() -> argparse.ArgumentParser:
    """Build ArgumentParser for Essentials CLI."""
    parser = argparse.ArgumentParser(
        prog="essentials",
        description="Essentials: Universal AI Developer Toolkit (portable Agent Skills, configs, templates).",
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # list
    p_list = subparsers.add_parser("list", help="List available skills, categories, and curated profiles")
    p_list.add_argument("--json", action="store_true", help="Output in machine-readable JSON format")
    p_list.set_defaults(func=cmd_list)

    # search
    p_search = subparsers.add_parser("search", help="Search available skills by keyword or category")
    p_search.add_argument("query", help="Search keyword")
    p_search.add_argument("--category", "-c", help="Filter by category (e.g. engineering, threejs, python)")
    p_search.add_argument("--json", action="store_true", help="Output in machine-readable JSON format")
    p_search.set_defaults(func=cmd_search)

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspect metadata, description, and manual-copy instructions")
    p_inspect.add_argument("skill_id", help="Skill ID or profile name")
    p_inspect.add_argument("--json", action="store_true", help="Output in machine-readable JSON format")
    p_inspect.set_defaults(func=cmd_inspect)

    # validate
    p_validate = subparsers.add_parser("validate", help="Validate skill directories, frontmatter, and uniqueness")
    p_validate.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_cli_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except CLIError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
