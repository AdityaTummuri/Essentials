# Mods

Mods change how Claude Code behaves or looks: hooks, slash commands, panels, and status lines. They can read your session, alter model routing, and show UI, so treat each one like code.

## Status

| Item | Status | Notes |
|---|---|---|
| `claude-mods.pdf` | Reference only | A guide with copy-paste prompts (Team Room, Saver, Dashboard), sample mods, and one-liners. Nothing from it is installed. |

## Rules for this folder

1. A mod is not installed by `scripts/setup-project.sh`. Installing one is a separate, reviewed step.
2. Do not enable a mod automatically. Read what it does first. Its hooks run on every tool call or prompt.
3. Anything Claude generates from a prompt in the PDF is new third-party code until you have read it. Keep generated mods out of this library until reviewed, then record them in `resources.json` with `kind: "mod"` and a `securityReview` entry.
4. Mods that route prompts to other models (for example Saver) change cost and data flow. Decide that deliberately.
5. Mods that read connectors (for example Dashboard reading Gmail and Calendar) expose that data to the mod. Scope the connectors first.

Mod plugin mechanics are documented in the built-in `plugin-authoring` skill and `claude plugin --help`.
