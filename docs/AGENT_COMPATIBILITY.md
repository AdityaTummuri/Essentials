# Agent Compatibility Guide

Essentials skills are built on the open **Agent Skills specification** (`SKILL.md` with standard YAML frontmatter `name` and `description`).

Because skills in Essentials are self-contained folders with zero proprietary installer dependencies, they are natively compatible with virtually every modern AI coding agent.

---

## 1. Compatibility Matrix

| AI Coding Agent | Compatibility | Global Skill Path | Project Skill Path | Setup Method |
|---|---|---|---|---|
| **OpenCode** | Native | `~/.agents/skills/` | `<project>/.agents/skills/` | Direct folder copy |
| **VS Code Copilot** | Native | `~/.agents/skills/` | `<project>/.agents/skills/` | Direct folder copy |
| **Gemini CLI / Antigravity** | Native | `~/.agents/skills/` | `<project>/.agents/skills/` | Direct folder copy |
| **OpenAI Codex** | Native | `~/.agents/skills/` | `<project>/.agents/skills/` | Direct folder copy |
| **Claude Code** | Native | `~/.claude/skills/` | `<project>/.claude/skills/` | Direct folder copy or symlink |
| **Cursor** | Native | `~/.agents/skills/` | `<project>/.agents/skills/` or `.cursor/rules/` | Direct folder copy |
| **Windsurf** | Native | `~/.agents/skills/` | `<project>/.agents/skills/` or `.windsurf/rules/` | Direct folder copy |

---

## 2. Agent-Specific Copy Instructions

### 1. OpenCode, VS Code with Copilot, Gemini CLI, & OpenAI Codex
All of these agents automatically discover skills placed in the standard `~/.agents/skills/` directory (or a local `.agents/skills/` inside a repository).

**Copy one skill:**
```bash
mkdir -p ~/.agents/skills
cp -r skills/engineering/code-review ~/.agents/skills/
```

**Copy an entire category (e.g. all 24 Three.js skills):**
```bash
cp -r skills/threejs/* ~/.agents/skills/
```

**Copy into the current workspace/repository only:**
```bash
mkdir -p .agents/skills
cp -r /path/to/Essentials/skills/python/pytest-workflow .agents/skills/
```

---

### 2. Claude Code
Claude Code looks for skills in `~/.claude/skills/<skill-id>/SKILL.md` or in the project's `.claude/skills/<skill-id>/SKILL.md`.

**Copy directly:**
```bash
mkdir -p ~/.claude/skills
cp -r skills/design/frontend-design ~/.claude/skills/
```

**Or share with `~/.agents/skills/` (Recommended):**
If you use multiple agents on the same machine, create a symlink once so skills copied to `~/.agents/skills/` are instantly recognized by Claude Code:
```bash
mkdir -p ~/.agents/skills
ln -s ~/.agents/skills ~/.claude/skills
```

---

### 3. Cursor & Windsurf
Modern versions of Cursor and Windsurf recognize the universal Agent Skills directory (`~/.agents/skills/` and `.agents/skills/`).

If you prefer project-local rules:
- **Cursor**: You can copy a skill into `.cursor/rules/<skill-id>/` or place the `SKILL.md` directly as a rule.
- **Windsurf**: Place the skill in `.windsurf/rules/<skill-id>/` or `.agents/skills/`.

---

## 3. Verifying Installation in Your Agent

After copying skill folders:

1. **Claude Code**: Type `/<skill-id>` (e.g. `/frontend-design`) or prompt Claude on the skill's subject. Claude will load the skill context automatically.
2. **VS Code Copilot / OpenCode**: The skills appear in the agent skill registry and are dynamically loaded when the user's prompt matches the skill description.
3. **Gemini CLI / Antigravity**: Scans active workspace and user directories automatically at startup.
