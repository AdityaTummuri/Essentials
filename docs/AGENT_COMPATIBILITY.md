# Agent Compatibility Matrix

Essentials aims for pragmatic, honest compatibility across AI coding agents. We distinguish between **Native Verified** (the agent discovers and parses the directory structure out of the box) and **Adapter-Mediated** (Essentials adapts the canonical skill into the format or location expected by the agent).

## Supported Agents Matrix

| Agent / Tool | Support Level | Discovery Path | Format | Verification Status |
|---|---|---|---|---|
| **Claude Code** | Native | `<project>/.claude/skills/<id>/`<br>`~/.claude/skills/<id>/` | Canonical `SKILL.md` (YAML frontmatter) | **Verified**. End-to-end unit, integration, and global setup tests passing. |
| **OpenCode** | Native | `<project>/.agents/skills/<id>/`<br>`~/.agents/skills/<id>/`<br>`~/.config/opencode/skills/<id>/` | Canonical `SKILL.md` (Agent Skills standard) | **Verified**. Native discovery in shared and dedicated paths. |
| **VS Code Copilot** | Native & Adapter | `<project>/.agents/skills/<id>/`<br>`~/.agents/skills/<id>/`<br>`~/.copilot/skills/<id>/`<br>`<project>/.github/prompts/<id>.prompt.md` | Canonical `SKILL.md` (global/workspace) or `.prompt.md` (repo prompt) | **Verified**. Global Agent Skills and workspace prompts supported. |
| **Gemini CLI / Antigravity** | Native | `<project>/.agents/skills/<id>/`<br>`~/.agents/skills/<id>/` | Canonical `SKILL.md` | **Verified**. Scanned and active in live workspaces. |
| **OpenAI Codex** | Native | `<project>/.agents/skills/<id>/` or `.codex/skills/` | Canonical `SKILL.md` | **Verified** with the open Agent Skills specification. |
| **Cursor** | Adapter | `<project>/.cursor/rules/<id>.mdc` | Markdown with Cursor MDC frontmatter (`globs`, `description`) | **Verified via Adapter**. Transforms canonical skills to `.mdc` rules. |
| **Windsurf** | Adapter | `<project>/.windsurf/rules/<id>.md` | Markdown rules file | **Verified via Adapter**. Converted to Cascade project rules. |

---

## Agent-Specific Implementation Details

### 1. Claude Code
- **Mechanism**: Claude Code natively inspects `<project>/.claude/skills/` and `~/.claude/skills/`.
- **Precedence**: Project-local skills override user-global skills with the same name.
- **Activation**: Type `/<skill-id>` in Claude Code chat or let the model auto-load relevant skills based on user prompt semantics.

### 2. Gemini CLI & Antigravity
- **Mechanism**: Looks in the active project workspace under `.agents/skills/<skill-id>/SKILL.md`.
- **Precedence**: Active project workspace skills take priority.
- **Activation**: Automatically indexed into the agent context if the skill metadata matches the user's intent.

### 3. Cursor
- **Mechanism**: Cursor IDE uses modern Cursor Rules (`.cursor/rules/*.mdc`) or legacy `.cursorrules`.
- **Adapter**: Essentials automatically generates `.cursor/rules/<skill-id>.mdc` with the required YAML frontmatter:
  ```yaml
  ---
  description: <Skill purpose and triggers>
  globs: *
  alwaysApply: false
  ---
  ```
- **Activation**: Triggered automatically when relevant files match, or referenced in Chat with `@rule-name`.

### 4. Windsurf
- **Mechanism**: Windsurf reads `.windsurf/rules/` or project-level `.windsurfrules`.
- **Adapter**: Essentials deploys skills as individual rules in `.windsurf/rules/<skill-id>.md` or appends managed blocks to `.windsurfrules`.

### 5. OpenCode
- **Mechanism**: OpenCode discovers Agent Skills globally from `~/.agents/skills/` (shared open standard) and `~/.config/opencode/skills/` (XDG dedicated), as well as project-level `.agents/skills/`.
- **Precedence**: Local workspace skills override global skills.
- **Activation**: Progressively indexed and dynamically loaded when the user's prompt matches the skill metadata.

### 6. GitHub Copilot & VS Code
- **Mechanism**: 
  - **Global / Personal Scope**: VS Code with GitHub Copilot scans `~/.agents/skills/` (the shared Agent Skills specification) and `~/.copilot/skills/`.
  - **Project / Workspace Scope**: Reads `.agents/skills/`, `.github/skills/`, and prompt instruction files in `.github/prompts/<id>.prompt.md`.
- **Adapter**: Supports both native Agent Skills directories and `.github/prompts/` workspace prompt files.


