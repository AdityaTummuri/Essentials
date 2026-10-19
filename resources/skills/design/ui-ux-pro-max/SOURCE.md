# Source: ui-ux-pro-max-skill

- Repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Commit: `56ea9cf174ed86786187daa9de0e6247cb0747e4` (2026-10-15)
- License: MIT (see `LICENSE` in this folder)
- Upstream path copied: `.claude/skills/ui-ux-pro-max/` and `.claude/skills/design/`
- Retrieved: 2026-10-19
- Modifications: none (verbatim copy; VCS metadata excluded)

## Included skills

| Folder | Purpose |
|---|---|
| `ui-ux-pro-max/` | Searchable UI/UX rules, palettes, typography and style data (`data/`, `scripts/`) |
| `design/` | Design-generation workflow and references |

## Not vendored (held for review)

- `.claude/skills/ui-styling/` — contains `shadcn_add.py` (runs `npx`/subprocess) and 5.8 MB of font files.
- `.claude/skills/design-system/` — `fetch-background.py` downloads images from the network; scripts spawn processes.
- `.claude/skills/brand/` — `sync-brand-to-tokens.cjs` uses `child_process`.
- `stack/.claude/settings.json` and `stack/scripts/setup.sh` — project settings and an installer; intentionally excluded.

## Scripts in included skills

`ui-ux-pro-max/scripts/` contains Python helpers. A static scan found no network calls or subprocess use in them. They are not run by the installer.
