# Multi-Agent Adapters

Essentials provides an extensible adapter framework allowing canonical agent skills to be deployed seamlessly across diverse AI agents, IDEs, and environments.

## How Adapters Work

1. **Canonical Source**: Every skill is stored once in `resources/skills/` following the Agent Skills specification (a directory containing `SKILL.md` with YAML frontmatter `name` and `description`).
2. **Deterministic Translation**: When a developer installs a skill or profile with `--agent <name>`, the designated adapter handles the transformation:
   - **Claude Code (`claude-code`)**: Links or copies the folder to `<project>/.claude/skills/<id>/`.
   - **Gemini CLI / Antigravity (`gemini-cli`)**: Links or copies the folder to `<project>/.agents/skills/<id>/`.
   - **OpenAI Codex (`codex`)**: Links or copies the folder to `<project>/.agents/skills/<id>/`.
   - **Cursor (`cursor`)**: Generates an MDC rule file at `<project>/.cursor/rules/<id>.mdc` with valid frontmatter (`globs: *`, `alwaysApply: false`).
   - **Windsurf (`windsurf`)**: Generates a Cascade rule file at `<project>/.windsurf/rules/<id>.md`.
   - **GitHub Copilot (`copilot`)**: Generates prompt instruction files at `<project>/.github/prompts/<id>.prompt.md`.
3. **Ledger & Uninstallation**: Every installed item records its adapter name in `.essentials-ledger.json`. When running `uninstall`, the corresponding adapter safely removes the installed file or symlink while ensuring user-edited files are preserved.

## Adding a New Adapter

To add support for a new agent:
1. Subclass `BaseAdapter` in a new module under `adapters/`.
2. Define `name`, `aliases`, `description`, and `discovery_path`.
3. Implement `get_destination_path`, `install`, `uninstall`, and `verify`.
4. Register the new adapter in `adapters/registry.py`.
