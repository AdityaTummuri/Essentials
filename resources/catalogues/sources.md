# External sources

Status key: **vendored** = copied into `skills/` and installable. **held** = needs your decision before copying. **catalogue** = link only. **dependency** = install in an app, not as a skill.

## Design and interface

| Source | Status | License | Notes |
|---|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | **held** | Apache-2.0 | Its `scripts/impeccable` downloads and runs a remote engine at runtime. Ships hooks. See [docs/SECURITY-REVIEW.md](../docs/SECURITY-REVIEW.md). |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | **partly vendored** | MIT | `ui-ux-pro-max` and `design` vendored. `ui-styling`, `design-system`, `brand` held (network and subprocess scripts). `stack/.claude/settings.json` excluded. |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | **partly vendored** | MIT | 8 motion skills vendored. 7 others left out as out of scope for web portfolio and dashboards. |
| [kylezantos/design-motion-principles](https://github.com/kylezantos/design-motion-principles) | **vendored** | MIT | Overlaps with `emil-design-eng`. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | **catalogue** | none published | No LICENSE file, so not copied. Install from source if you accept its terms. |
| [moesuito/claude-skill-design-md](https://github.com/moesuito/claude-skill-design-md) | **vendored** | Apache-2.0 | `design-md`. |
| [zhuyansen/awesome-claude-design-skills](https://github.com/zhuyansen/awesome-claude-design-skills) | **catalogue** | CC0-1.0 | Daily-updated list. Link rather than copy. |
| [wilwaldon/Claude-Code-Frontend-Design-Toolkit](https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit) | **catalogue** | none published | README-only link list. No code. |

## Three.js and creative engineering

| Source | Status | License | Notes |
|---|---|---|---|
| [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) | **vendored** (primary) | MIT | All 24 skills. |
| [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) | **catalogue** | MIT | Alternative. See [threejs-alternatives.md](threejs-alternatives.md). |
| [oil-oil/oil-motion](https://github.com/oil-oil/oil-motion) | **held** | MIT | Credential-handling scripts, pip installs, and a CI workflow that uses sudo. Needs a full read. |
| [goldfire/howler.js](https://github.com/goldfire/howler.js) | **dependency** | MIT | Web audio library for app code. `npm install howler` in the project that needs it. Not a skill. |

## General skills and discovery

| Source | Status | License | Notes |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | **partly vendored** | Apache-2.0 for `frontend-design`; proprietary for `docx`, `pdf`, `pptx`, `xlsx` | `frontend-design` vendored. Document skills not copied; the platform already provides them. |

## Mods

| Source | Status | Notes |
|---|---|---|
| `mods/claude-mods.pdf` (local) | **unreviewed** | Copy-paste prompts for Team Room, Saver, and Dashboard mods, plus sample mods. Each would run inside Claude Code and could add hooks or UI. See [mods/README.md](../mods/README.md). |
| `anthropics/claude-code-playground` (named in the PDF) | **not reviewed** | Sample mods (`blast-radius`, `token-weather`, `replay-theater`). Not in your source list; not fetched. |
