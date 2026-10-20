# Architecture of Essentials

## 1. "Skills Are Just Folders" Architecture

Essentials is an all-in-one developer toolkit. Rather than requiring complex runtime installers, symlink managers, platform-specific translation adapters, or installation ledgers, the skills system operates on a simple, universal principle:

> **Skills are just folders.**

Any developer can clone or download Essentials, open the `skills/` directory, select any skill folder, and copy it directly into their agent's skills directory.

```text
Essentials/
├── skills/                      # Canonical, ready-to-copy skills library (82 skills)
│   ├── threejs/                 # 24 3D WebGL, shaders, performance & WebGPU skills
│   ├── engineering/             # 25 engineering, planning, debugging, security & code-review skills
│   ├── design/                  # 14 UI/UX, typography, design systems & motion skills
│   ├── robotics-ml/             # 7 computer vision, edge AI, dataset, ROS 2 & embedded skills
│   ├── python/                  # 5 modern Python typing, testing & packaging skills
│   ├── audio/                   # 1 browser audio & Web Audio API skill
│   ├── product/                 # 2 product strategy & UI design system skills
│   └── testing/                 # 4 visual regression, web app testing, E2E generation & coverage audit skills
├── configs/                     # Portable developer configs (Bash, Zsh, Git, EditorConfig)
├── templates/                   # Production-ready starter templates (Python, Web, Dashboards)
├── docs/                        # Architecture, compatibility, profiles, and audits
├── resources/                   # Integrity catalog (resources.json) & research
├── scripts/                     # Lightweight companion CLI (essentials)
├── tests/                       # Automated validation & unit test suite
├── README.md                    # Quickstart & copy-paste instructions
├── CONTRIBUTING.md              # Skill authoring & verification guide
├── SECURITY.md                  # Security policies & held resource audits
└── LICENSE                      # MIT License
```

---

## 2. Universal Agent Skills Standard

All skills in Essentials adhere strictly to the open **Agent Skills** specification:

```text
skills/<category>/<skill-id>/
├── SKILL.md                 # Primary instruction guide with YAML frontmatter
└── (supporting assets)      # Optional references, templates, recipes, checklists
```

### Format Specification
Each `SKILL.md` starts with standard YAML frontmatter:
```markdown
---
name: code-review
description: "Comprehensive code review guidelines for spotting architectural flaws, performance bottlenecks, and security vulnerabilities."
---

# Code Review Guidelines
...
```

### Discovery Paths across Modern Agents
Modern AI coding assistants recognize this standard out of the box:

| AI Coding Agent | Global / Personal Discovery Path | Project-Local Discovery Path |
|---|---|---|
| **OpenCode** | `~/.agents/skills/<skill-id>/` | `<project>/.agents/skills/<skill-id>/` |
| **VS Code Copilot** | `~/.agents/skills/<skill-id>/` | `<project>/.agents/skills/<skill-id>/` |
| **Gemini CLI / Antigravity** | `~/.agents/skills/<skill-id>/` | `<project>/.agents/skills/<skill-id>/` |
| **OpenAI Codex** | `~/.agents/skills/<skill-id>/` | `<project>/.agents/skills/<skill-id>/` |
| **Claude Code** | `~/.claude/skills/<skill-id>/` | `<project>/.claude/skills/<skill-id>/` |
| **Cursor / Windsurf** | `~/.agents/skills/<skill-id>/` | `<project>/.agents/skills/<skill-id>/` |

Because `~/.agents/skills/` is the emerging universal standard, copying skills there makes them immediately available across OpenCode, GitHub Copilot, Gemini CLI, OpenAI Codex, and others. For Claude Code, users can either copy directly to `~/.claude/skills/` or create a one-time directory link:
```bash
ln -s ~/.agents/skills ~/.claude/skills
```

---

## 3. Companion CLI Architecture (`./scripts/essentials`)

To assist developers without imposing any mandatory runtime dependencies or modifying files unexpectedly, Essentials includes a zero-dependency Python standard library companion CLI:

```bash
./scripts/essentials list             # Browse all 82 skills across 8 categories and profiles
./scripts/essentials search <query>    # Search skills by keyword, category, or triggers
./scripts/essentials inspect <id>      # View skill details, frontmatter, paths, and copy command
./scripts/essentials inspect <profile> # View all skills and copy command for a curated profile
./scripts/essentials validate          # Run static verification checks on the entire library
```

### Design Invariants
1. **Zero Pip Dependencies**: Runs immediately with standard `python3` on any modern OS.
2. **Read-Only Inspection**: `list`, `search`, and `inspect` never alter your files, home directory, or git status.
3. **Copy-Command Generation**: `inspect` outputs the exact `cp -r` command so you stay in total control.
4. **No Installation Ledgers**: Because skills are plain folders copied by the user, there is no fragile state machine or ledger to corrupt.

---

## 4. Integrity, Cataloging & Security Model

Even though skills are just folders for the end user, Essentials enforces strict repository engineering standards to protect against supply-chain vulnerabilities:

### Authoritative Manifest (`resources/resources.json`)
The catalog tracks every skill's provenance:
- **Canonical ID & Category**: Unique skill name and functional category.
- **Relative Path**: Location within `skills/<category>/<skill-id>`.
- **Upstream Source**: Git URL, pinned commit hash, and commit date.
- **License**: SPDX license identifier (MIT, Apache-2.0).
- **Security Review Status**: `static-reviewed` classification confirming pure markdown guidance with zero background execution.
- **Cryptographic SHA-256**: Hash of every `SKILL.md` to detect accidental drift or tampering.

### Forbidden Artifacts Enforcement
`./scripts/essentials validate` and `tests/test_catalog.py` enforce strict security hygiene:
- No hidden execution hooks: `hooks.json`, `settings.json`, `settings.local.json`.
- No unreviewed MCP server configurations: `.mcp.json`.
- No extraneous `.claude-plugin/` or binary executables.
- Valid YAML frontmatter with non-empty `name` and `description` on every skill.
- 100% unique skill names across all categories.

---

## 5. Non-Skill Capabilities in the Toolkit

Essentials is an all-in-one developer toolkit, not just a skills directory:

- **Developer Configurations (`configs/`)**: Battle-tested shell dotfiles for Bash, Zsh, Git aliases, and `.editorconfig`.
- **Starter Templates (`templates/`)**: Production-ready scaffolding for Python applications, creative WebGL projects, and data dashboards.
- **Documentation (`docs/`)**: In-depth agent compatibility matrix, profile guides, and upstream maintenance logs.
- **Automated CI (`.github/workflows/test.yml`)**: Continuous integration testing verifying skill structure, manifest integrity, and CLI commands.
