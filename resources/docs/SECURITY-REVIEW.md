# Security review record

Reviewed 2026-10-19 against the commits pinned in `resources.json`. The method was static: frontmatter checks, a scan for hooks, settings, and plugin manifests, and a scan of scripts for network, exec, subprocess, and credential patterns. Nothing was executed.

## Vendored (installable)

| Collection | Result |
|---|---|
| `design/ui-ux-pro-max` (`ui-ux-pro-max`, `design`) | Static-reviewed. `ui-ux-pro-max/scripts/` has local Python helpers. No network or subprocess calls found in them. The installer never runs them. |
| `design/design-md` | Static-reviewed. Markdown and templates only. |
| `frontend/frontend-design` | Static-reviewed. Markdown only. |
| `motion/emil-design-eng` (8 skills) | Static-reviewed. Markdown only. |
| `motion/design-motion-principles` | Static-reviewed. Markdown and reference files only. |
| `threejs/cesartevisual-threejs-skills` (24 skills) | Static-reviewed. Markdown only. No scripts, hooks, or settings. |

The validator (`scripts/setup-project.sh --validate`) blocks any vendored `settings.json`, `settings.local.json`, `hooks.json`, `.mcp.json`, `plugin.json`, `.claude-plugin/`, or `.git/`. It also blocks symlinks inside the library, and fails if a vendored `SKILL.md` no longer matches its recorded hash.

## Held: needs your decision

| Item | Why held | Options |
|---|---|---|
| **impeccable** | `scripts/impeccable` fetches a remote engine with `curl` or `wget` and runs it. Its checksum check reads a `.sha256` file fetched from the same URL with `.sha256` appended, so it does not protect against a compromised host. Its `plugin/hooks/hooks.json` defines hooks. | (a) Vendor the SKILL and `reference/` only, with scripts removed. The skill would lose its CLI. (b) Vendor everything, pinned, after you accept that the engine is downloaded at runtime. (c) Skip. |
| **oil-motion** | Contains `secure_credentials.py` and a `credential-ui/` folder. SKILL.md has `pip install` steps. The CI workflow uses sudo. | Full read of the scripts before any vendoring. |
| **ui-styling** | `scripts/shadcn_add.py` runs `npx` through subprocess. 5.8 MB of font files. | Vendor SKILL and references only, or whole. |
| **design-system** | `scripts/fetch-background.py` downloads images from pexels.com. Scripts spawn processes. | Vendor after reviewing the download behavior, or skip. |
| **brand** | `scripts/sync-brand-to-tokens.cjs` uses `child_process.execFileSync`. | Same as above. |

## Not vendored: license

| Item | Reason |
|---|---|
| `vercel-labs/agent-skills` | No LICENSE file. |
| `wilwaldon` toolkit | No LICENSE file; README-only. |
| `anthropics/skills` document skills (`docx`, `pdf`, `pptx`, `xlsx`) | Proprietary terms. The platform already provides them. |

## Not installed: out of scope

`CloudAI-X/threejs-skills` (duplicates the primary set), `howler.js` (application dependency), `zhuyansen` list (catalogue).

## Mods

`mods/claude-mods.pdf` is a prompt guide. It is not installed. Each mod it describes needs review first (see [mods/README.md](../mods/README.md)).

## Installer boundaries

- Writes only inside `<project>/.claude/skills/` and its own ledger `<project>/.claude/.resources-library.json`.
- Never writes `CLAUDE.md`, `settings*.json`, global `~/.claude`, or plugin configuration. It reads `~/.claude/skills` only to warn about name clashes.
- Refuses to overwrite anything it did not create. Conflicts abort the whole run before any change.
- Uninstall removes only installs recorded in the ledger, and only if the link still points to the library, or the copy still matches its recorded hash.
