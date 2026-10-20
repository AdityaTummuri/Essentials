# Agent Toolkit

What is set up for each AI agent on this machine, which parts each agent can use, and where each piece lives. Verified state, side effects, and pending steps are in [INSTALLATION_STATUS.md](INSTALLATION_STATUS.md). The full skill list with licences and safety flags is in [SKILL_CATALOG.md](SKILL_CATALOG.md).

Three kinds of thing are tracked separately:

1. **Skills**: folders copied into an agent's skills directory. Plain files, no runtime.
2. **Plugins**: packages installed through an agent's own plugin system.
3. **MCP servers**: tool servers an agent starts and talks to.

Models (Ollama) are a fourth kind and are listed separately.

## Claude Code (v2.1.304)

| Component | Kind | Scope | Status |
| --- | --- | --- | --- |
| Superpowers 7.0.0 | Plugin (`superpowers@claude-plugins-official`) | user | Installed, enabled. Adds a SessionStart hook |
| Playwright MCP (`@playwright/mcp@latest`, npm 0.0.83) | MCP server | user | Connected. Chromium not downloaded (awaiting approval) |
| Context7 MCP (`https://mcp.context7.com/mcp`) | MCP server | user | Connected. Docs lookup verified. **Confirm the device approval in your Context7 dashboard** (see INSTALLATION_STATUS 1.1) |
| Context7 rule and skill | Rule (`~/.claude/rules/context7.md`) and skill (`~/.claude/skills/context7-mcp/`) | user | Installed by the Context7 setup. The rule applies to every session |
| claude.ai Claude Docs | MCP server | built-in | Connected |
| design plugin MCPs (Slack, Figma, Linear, Atlassian, Notion, Intercom) | MCP servers | plugin | Pre-existing. Need authentication. Not changed |
| Personal skills | Skill folders | `~/.claude/skills/` | 66 Essentials folders, all identical to `skills/` |

Not copied into `~/.claude/skills/`, on purpose:

- The five Superpowers skills, the Superpowers plugin provides them.
- `skill-creator`, the platform provides it.
- `caveman`, which changes response style when activated.

## OpenCode (v1.19.0)

| Component | Kind | Status |
| --- | --- | --- |
| OpenCode binary | Agent | Present at `~/.opencode/bin/opencode`. Not on `PATH`. Config at `~/.config/opencode/opencode.json` |
| Personal skills | Skill folders | `~/.agents/skills/`: 75 Essentials folders, all identical to `skills/`. Every installed folder is discovered by OpenCode (`opencode debug skill`) |
| Oh My OpenAgent | OpenCode plugin | **Not installed.** Recommendation: defer (INSTALLATION_STATUS section 8) |
| `opencode.json` | Config | Rewritten by OpenCode on startup: added `"$schema"` and `"enabled": true` on the `rea` MCP entry. The command is unchanged. Decision pending |

## GitHub Copilot

| Component | Status |
| --- | --- |
| Copilot CLI | **Not installed** (`copilot` not on `PATH`). `~/.copilot/mcp-config.json` already exists with a `rea` MCP entry; left untouched |
| VS Code Copilot | Not checked on this machine. The repository's compatibility notes say it reads `~/.agents/skills/`; that is not verified here |
| GitHub CLI (`gh` 2.45.0) | Installed and authenticated (keyring). Read-only repository and PR commands work. Credentials were not read or printed |

## Gemini CLI / Antigravity

| Component | Status |
| --- | --- |
| Gemini CLI | **Not installed** (`gemini` not on `PATH`). `~/.gemini/settings.json` exists with a `rea` MCP entry; left untouched |
| Antigravity | `~/.gemini/antigravity*` directories present. Not checked; no changes made |

## Local models (Ollama 0.40.4)

Three models are installed, about 10.7 GB on disk in total:

| Model | Size on disk |
| --- | --- |
| `hf.co/HauhauCS/Qwen3.5-2B-Uncensored-HauhauCS-Aggressive:Q6_K` | 2.2 GB |
| `hf.co/mradermacher/Huihui-Qwen3-8B-abliterated-v2-GGUF:Q4_K_M` | 5.0 GB |
| `hf.co/mradermacher/Huihui-Qwen3.5-4B-abliterated-GGUF:Q5_K_M` | 3.5 GB |

No model was downloaded during this setup. The `ollama-local-models` skill covers sizing and comparing them. The GPU is an RTX 4050 Laptop with 6 GB VRAM; the machine has 14 GB RAM.

## Shared skill library

The canonical copies live in `skills/` in this repository. Personal copies are real directories, not symlinks, so each agent reads files directly and nothing depends on this checkout's path. Every personal copy was compared with its repo source; all are identical.

- `~/.agents/skills/`: 75 skills. Read by OpenCode and by agents that use the shared location.
- `~/.claude/skills/`: 66 skills. Read by Claude Code.

`reverse-engineer-anything` was the untracked folder in `skills/`. It is now in `skills/engineering/`, unchanged, and is also installed in `~/.agents/skills/`.

## Not in this toolkit

- `caveman`: in the library, not copied to personal directories (opt-in).
- `using-git-worktrees` and `finishing-a-development-branch` (Superpowers): not vendored. Automation of worktree dependency installs and branch merges and deletes needs confirmation. See SKILL_CATALOG and UPSTREAM_AUDIT.
- Oh My OpenAgent: not installed. See INSTALLATION_STATUS section 8.
