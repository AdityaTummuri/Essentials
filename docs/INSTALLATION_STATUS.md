# Installation Status

Snapshot from 2026-10-20 on this machine (Fedora, user `aditya`). Each line says how it was verified. Anything not verified at runtime is labelled as such.

Companion documents: [AGENT_TOOLKIT.md](AGENT_TOOLKIT.md) (what each agent can use), [SKILL_CATALOG.md](SKILL_CATALOG.md) (every skill, its upstream, licence, and flags), and [UPSTREAM_AUDIT.md](UPSTREAM_AUDIT.md) (acquisition and exclusion decisions).

## 1. Verified and installed

| Item | Kind | Version / source | Verified by |
| --- | --- | --- | --- |
| Superpowers | Claude Code plugin | 7.0.0, `superpowers@claude-plugins-official`, user scope, enabled | `claude plugin list` (enabled) |
| Playwright MCP | MCP server (Claude Code) | `@playwright/mcp@latest`, npm 0.0.83, user scope | `claude mcp list`: Connected. Browser not downloaded |
| Context7 MCP | MCP server (Claude Code) | `https://mcp.context7.com/mcp`, HTTP, user scope | `claude mcp list`: Connected. Docs lookup returned results (section 2) |
| Context7 CLI | Tool | `ctx7` via `npx`, logged in | `npx ctx7 whoami` reports "Logged in". Library lookup returned react.dev |
| Personal skills, Claude Code | Skill folders | 66 Essentials folders in `~/.claude/skills/` | Every folder compared with `skills/` (identical) |
| Personal skills, shared | Skill folders | 75 Essentials folders in `~/.agents/skills/` | Every folder compared with `skills/` (identical). `opencode debug skill` lists all of them |
| Skill catalog | Repository file | `resources/resources.json`: 82 vendored skills | `tests/test_catalog.py` |
| `gh` CLI | Tool | 2.45.0, authenticated (keyring) | `gh auth status`; read-only `gh repo view` and `gh pr list` both work (no open PRs) |
| Git, Node, npm, Python | Tools | git 2.43.0, node v24.22.0, npm 11.19.1, Python 3.12.3 | `--version` |
| Claude Code | Agent | 2.1.304 | `claude --version` |
| OpenCode | Agent | 1.19.0 at `~/.opencode/bin/opencode` (not on `PATH`) | `opencode --version` |
| Ollama | Local model runtime | 0.40.4, server responding on `127.0.0.1:11434` | `ollama --version`, `/api/version` |

### 1.1 Context7: authorization event (read this)

Context7 setup ran as `npx ctx7 setup --claude --mcp`. Its output showed a one-time device code and an approval link, then reported "Authenticated with API key" within the same run. I did not open the link or enter the code, and I did not bypass any step. The CLI wrote `~/.config/context7/credentials.json` (permissions `600`) at 11:46.

Please confirm in your Context7 dashboard (https://context7.com/dashboard) that a device or session was authorised by you. If not, revoke the key there, then run `npx ctx7 logout` and `claude mcp remove context7 -s user`.

What the setup changed:

- `~/.claude.json`: `mcpServers.context7` added (HTTP, with an `Authorization` header holding the API key). The key is in your user configuration, not in the repository.
- `~/.claude/rules/context7.md` (new, 1.8 KB): a global rule telling every Claude Code session to prefer Context7 for library and API questions.
- `~/.claude/skills/context7-mcp/SKILL.md` (new, 2.7 KB): the Context7 skill.

Verification performed: `npx ctx7 library react "useEffect cleanup function"` returned `/reactjs/react.dev`. A headless `claude -p` call restricted to `mcp__context7__*` tools answered with library ID `/websites/react_dev_reference_react`.

### 1.2 Superpowers note

The plugin adds a `SessionStart` hook that loads its bootstrap into every Claude Code session. That is the plugin's design. Disable with `claude plugin disable superpowers@claude-plugins-official`.

## 2. Repository changes (uncommitted)

Skill count: **82 skills in `skills/`**, all validated, in 8 categories. Per category: `threejs` 24, `design` 14, `engineering` 25, `robotics-ml` 7, `python` 5, `testing` 4, `product` 2, `audio` 1. Counting rules are in the README and `docs/SKILL_CATALOG.md`.

New skills (26 in this change set counting `reverse-engineer-anything`, which was moved in):

| Category | Skills |
| --- | --- |
| `engineering/` | writing-plans, brainstorming, executing-plans, subagent-driven-development, verification-before-completion, receiving-code-review, requesting-code-review, systematic-debugging, acquire-codebase-knowledge, threat-model-analyst, secret-scanning, github-actions-hardening, dependabot, refactor, mcp-builder, skill-creator, caveman, ollama-local-models, reverse-engineer-anything (moved from the untracked folder) |
| `testing/` | webapp-testing, test-gap-audit, playwright-generate-test |
| `design/` | web-design-reviewer |
| `robotics-ml/` | ros2-debugging, esp32-embedded-debugging, pytorch-experiments |

Other changed files:

- `resources/resources.json`: provenance entries for every vendored skill. Five python entries gained their missing `skillMd.sha256`. `safeForDefault` corrected: `design` changed to `false`, `brainstorming`, `skill-creator`, and the two shell-script skills are `false`, and `ui-ux-pro-max` remains `true` after audit. `updated` is 2026-10-20.
- `skills/engineering/SOURCE.md`, `skills/testing/SOURCE.md`, `skills/design/SOURCE.md`, `skills/robotics-ml/SOURCE.md`: provenance tables and corrected safety statements.
- `tests/test_catalog.py`: six checks (catalog coverage, unique ids, SKILL.md hashes, the `safeForDefault` rule for code-bearing skills, no forbidden artifacts, no symlinks).
- `README.md`, `CHANGELOG.md`, `SECURITY.md`, `docs/ARCHITECTURE.md`, `docs/PROFILES.md`, `docs/UPSTREAM_AUDIT.md`: counts and wording corrected, new skills listed, acquisition decisions recorded.
- `docs/SKILL_CATALOG.md`, `docs/AGENT_TOOLKIT.md`, `docs/INSTALLATION_STATUS.md`: new.
- `skills/reverse-engineer-anything/` moved to `skills/engineering/reverse-engineer-anything/`. Content unchanged; byte-identical to the rea-agents 6.5.0 bundle.

## 3. Personal agent directories

- Replaced 51 dangling symlinks in each of `~/.agents/skills/` and `~/.claude/skills/`. They pointed at `resources/skills/...`, which no longer exists. Each was replaced by a real copy of the same-named repo skill. The manifest of old targets is at `~/.claude/backups/essentials-setup-2026-10-20/dangling-links-backup.txt`.
- `~/.agents/skills/`: added `brainstorming`, `subagent-driven-development`, and `executing-plans` (plus the earlier 20). Superpowers' five other skills are there too. Total 75 Essentials folders, all identical to the repo.
- `~/.claude/skills/`: no new Essentials skills in this pass. The Superpowers plugin provides its skills to Claude Code. `skill-creator` is provided by the platform. `caveman` is not copied anywhere; it changes response style when activated.
- Not Essentials: `~/.claude/skills/context7-mcp/` (installed by the Context7 setup), `synced/`, and `.trash/` (pre-existing).

## 4. Configuration backups and side effects

Stored under `~/.claude/backups/essentials-setup-2026-10-20/` (`600` where the file may hold credentials):

- `claude.json.backup`, `claude-settings.backup.json`: taken before the Playwright and Superpowers changes.
- `claude.json.pre-context7.backup`, `claude-settings.pre-context7.backup.json`: taken before the Context7 setup.
- `dangling-links-backup.txt`: 102 lines of old link targets.

Side effects you should know about:

- **OpenCode config rewritten by OpenCode.** `~/.config/opencode/opencode.json` was modified at 11:31 today. OpenCode rewrote it on startup when I ran `opencode debug skill` to verify skill discovery. The file now has a `"$schema"` key and `"enabled": true` on the `rea` MCP entry. The `rea` command is unchanged. I did not take a backup before that command, so I cannot restore the exact original bytes. Removing those two keys would restore the meaning. Tell me if you want that done.
- `~/.claude.json`: Claude Code's own cache keys changed, as usual. The Context7 and Playwright entries are the only intended changes.
- `~/.claude/settings.json`: unchanged by the Context7 setup. The Superpowers plugin entry (`enabledPlugins`) was added earlier.
- No changes to `~/.gemini`, `~/.copilot`, shell configuration, or system packages.

## 5. Test and validation results (final run)

- `./scripts/essentials validate`: **82 skills across 8 categories, 0 errors, 0 warnings.** The earlier untracked-folder error is resolved by moving the folder into `engineering/`.
- `python3 -m unittest discover -s tests -v`: **15 tests, 15 passed, 0 failed.** Nine are the original suite (including the two validator tests that failed before the move). Six are in `tests/test_catalog.py`.
- Repository secret scan (credential-shaped strings such as GitHub tokens, `sk-` keys, AWS keys, `Bearer` values, and the device code) across the 138 changed and new files: no matches.
- Large files: none over 1 MB in the changed set.
- Personal installs: every folder in both directories compared with the repo. `~/.agents/skills/`: 75 identical, 0 differ, 0 symlinks. `~/.claude/skills/`: 66 identical, 0 differ, 0 symlinks, plus `context7-mcp` (Context7, not from this repo) and `synced/` (pre-existing).
- OpenCode skill discovery: every installed folder in `~/.agents/skills/` appears in `opencode debug skill` (run before the config rewrite noted in section 4).

## 6. Browser: Playwright (prepared, not downloaded)

The MCP server is connected. It runs headed by default and accepts `--headless`. Chromium is not downloaded and no browser cache exists at `~/.cache/ms-playwright`.

Download sizes, measured from the CDN with HTTP `HEAD` requests (no payload transferred):

| Download | Size | Needed for |
| --- | --- | --- |
| Chrome for Testing (`chromium`) | 191.1 MiB | Headed and headless use |
| Chrome Headless Shell (`chromium-headless-shell`) | 120.0 MiB | Headless use only |
| FFmpeg | 2.2 MiB | Video recording |

Options, awaiting your approval:

- Headless only (about 122 MiB): `npx playwright install chromium-headless-shell`, then start the MCP with `--headless`.
- Headed and headless (about 313 MiB): `npx playwright install chromium`.

Neither command uses `sudo`. Do not use `--with-deps`, which installs system packages. Playwright installs under `~/.cache/ms-playwright`. Installed size is larger than the download; I did not measure it.

## 7. Not installed, and why

| Item | Reason | Next action |
| --- | --- | --- |
| Oh My OpenAgent | See section 8 | Recommendation: defer |
| Gemini CLI | Not installed on this machine | Install if wanted. Skills would go in `~/.agents/skills/`, which Gemini reads per the repo's notes (not verified here) |
| GitHub Copilot CLI | Not installed on this machine | Same as Gemini |
| Chromium browser | Awaiting approval (section 6) | Approve one of the two options |
| `using-git-worktrees`, `finishing-a-development-branch` (Superpowers) | `finishing` merges, pushes, and force-deletes branches. `worktrees` runs `npm install` / `pip install` automatically in each new worktree. Both are unsafe to automate without confirmation. Adopted skills reference them; the Superpowers plugin supplies them to Claude Code | None, unless you want them vendored |
| `skill-creator` in personal directories | Platform provides it to Claude Code. Its scripts call `claude -p` | None |
| Caveman proxy, hooks, installer | Excluded by the brief | None |
| Anthropic `frontend-design` | Already vendored in `skills/design/frontend-design`. Duplicate avoided | None |

## 8. Oh My OpenAgent: recommendation (not installed)

**Purpose.** An OpenCode plugin ("Ultimate" edition, package `oh-my-openagent`). It adds agent orchestration, agent and model routing, and built-in MCP tools (web search via Exa, GitHub search, Context7 docs). Its upstream guide and README describe it as a plugin that loads into an existing OpenCode install.

**Current supported installation** (from the upstream installation guide on its `dev` branch): `bunx oh-my-openagent install`, a terminal UI that walks through setup. The guide says not to use `npm install -g`, `bun add -g`, or `bun install -g`. The guide also suggests letting an agent perform the install. This setup did not do that.

**What the installer changes:**
- Registers the plugin in `~/.config/opencode/opencode.json` (the `plugin` array).
- Writes agent and model configuration and provider authentication.
- The related `omo setup` flow (OmO Native and migration paths) imports API keys, MCP servers from existing OpenCode config, and model settings after a single consent. Read the summary before consenting. `--dry-run` shows it without writing.
- Adds a comment-checker binary, downloaded from GitHub releases on first use.

**Telemetry.** Anonymous telemetry is enabled by default, with one event per UTC day per machine. Opt out before installing by setting `OMO_SEND_ANONYMOUS_TELEMETRY=0` or `OMO_DISABLE_POSTHOG=1` in the environment for the install. Do not add them to shell profiles unless you want them persistent, and do not change shell configuration as part of this setup.

**Licence.** Sustainable Use License 1.0, not MIT. Use is limited to internal business or non-commercial purposes, and redistribution must be free and non-commercial. Third-party components keep their own licences.

**Recommendation.** Defer. Reasons:
1. OpenCode is installed but not on `PATH`. Confirm you use it before adding a plugin to it.
2. The install edits your OpenCode configuration and can import credentials. Back up `~/.config/opencode/opencode.json` first.
3. The licence does not allow commercial use.

If you decide to proceed later: opt out of telemetry in the environment, back up the OpenCode config, run `bunx oh-my-openagent install` yourself, and decline credential and MCP imports unless you want them. Then check `~/.config/opencode/opencode.json` and remove anything you did not intend.

## 9. Manual steps for you

1. **Context7 authorization check.** Confirm the device approval in your dashboard (section 1.1). Revoke if it was not you.
2. **Chromium.** Approve one of the two options in section 6, then I will run it. Or run it yourself with `! npx playwright install chromium-headless-shell`.
3. **Oh My OpenAgent.** Decide whether to pursue it later (section 8).
4. **OpenCode config.** Tell me whether to remove the `"$schema"` key and `"enabled": true` that OpenCode added on startup.
5. **ESP32 serial access.** If a serial device returns permission denied, add your user to `dialout` yourself (`sudo usermod -aG dialout $USER`, then log out and back in). This setup did not use `sudo`.
6. **Design generators.** Decide whether to hold the `design` skill's image-generation scripts (section 10).

## 10. Known issues and decisions outstanding

- **`design` generators.** The skill is in the library but flagged `safeForDefault: false`. Its logo, icon, and CIP generators call external APIs and read `.env` files. SECURITY.md's held-resource rule would exclude them. Decision: keep, strip the API scripts, or hold the whole skill.
- **`python-dev` preset mismatch.** `resources/resources.json` lists `code-review`, `test-driven-development`, `git-hygiene`, `api-design`, and `security-audit`. `docs/PROFILES.md` describes the Python skills plus `code-review`, `git-hygiene`, and `security-audit`, and its copy command uses those. The two disagree. The preset was not changed; decide which is intended.
- **Dangling references in adopted skills.** `finishing-a-development-branch` and `using-git-worktrees` are referenced but not vendored (section 7). In non-Claude agents, those references do not resolve.
- **`${CLAUDE_PLUGIN_ROOT}` paths.** `ui-ux-pro-max`'s SKILL.md examples point at `${CLAUDE_PLUGIN_ROOT}/.claude/skills/...`. That variable is not set for personal installs, so those examples will not run as written.
- **Executable bit on Markdown.** `product-strategist` and `ui-design-system` have `755` on their `SKILL.md`. Harmless, but not intended. Not changed.
- **Historical numbers.** `CHANGELOG.md` entries for 3.0.0 and earlier still say 56 skills. Those are release records and were left as written.
- **Playwright install size.** Installed size is not measured (section 6).
