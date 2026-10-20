# Universal Engineering Skills Collection

- **Origin**: Essentials Canonical Engineering Suite
- **License**: MIT
- **Maintained By**: Essentials maintainers
- **Date Added**: 2026-10-20
- **Scope**: Static, declarative markdown instructions for software craftsmanship, code reviews, TDD, and Git hygiene.
- **Safety**: Mostly Markdown instructions. Several skills bundle scripts (Python, shell, or Node). Each is marked `safeForDefault: false` in `resources/resources.json` and runs only when a user asks the agent to use it. See the provenance section below.

## Third-party provenance

Skills in this folder that were not written by Essentials. Upstream licence and attribution are kept with each skill (`LICENSE.txt` where the upstream ships one). Acquired 2026-10-20.

| Skill | Upstream | Commit | Licence | Notes |
| --- | --- | --- | --- | --- |
| writing-plans, verification-before-completion, receiving-code-review, requesting-code-review, systematic-debugging | [obra/superpowers](https://github.com/obra/superpowers) | `bb92a77` (2026-10-09) | MIT | Markdown only. Excluded: `brainstorming` and `subagent-driven-development` (bundled servers and shell scripts pending review), `find-polluter.sh`, TypeScript example. |
| acquire-codebase-knowledge, threat-model-analyst, secret-scanning, github-actions-hardening, dependabot, refactor | [github/awesome-copilot](https://github.com/github/awesome-copilot) | `613efc8` (2026-10-20) | MIT | `acquire-codebase-knowledge` bundles `scripts/scan.py` (read-only git commands). |
| mcp-builder | [anthropics/skills](https://github.com/anthropics/skills) | `dbd4588` (2026-10-09) | Apache-2.0 (`LICENSE.txt`) | Bundled Python evaluation harness calls the Anthropic API with the user's own key. |
| caveman | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `bad48a0` (2026-10-17) | Apache-2.0 (`LICENSE.txt`; upstream `NOTICE` applies) | Lightweight skill only. Excluded: proxy, middleware, shell hooks, installer. |
| ollama-local-models | Essentials (original) | n/a | MIT | Written for this repository. |
| brainstorming, subagent-driven-development, executing-plans | [obra/superpowers](https://github.com/obra/superpowers) | `bb92a77` (2026-10-09) | MIT | Scripts included. `brainstorming` ships a localhost companion server (Node stdlib, token-protected, opt-in browser open). `subagent-driven-development` and `executing-plans` ship shell helpers that use read-only git commands and write under `.superpowers/sdd/`. |
| skill-creator | [anthropics/skills](https://github.com/anthropics/skills) | `dbd4588` (2026-10-09) | Apache-2.0 (`LICENSE.txt`) | Bundled Python runs `claude -p` for evaluations and starts a localhost-only review server. |
| reverse-engineer-anything | [morluto/rea](https://github.com/morluto/rea), npm `rea-agents` 6.5.0 (tag `rea-agents-6.5.0` = `3b79af28`) | MIT | Byte-identical to the rea-agents bundled skill. Moved from the untracked `skills/` folder. Markdown only. Instructs the agent to run `npx rea-agents@6.5.0`, and after approval to write MCP client configuration. |
