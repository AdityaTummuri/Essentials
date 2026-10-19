# Claude Code resource library

A central, reviewed library of Claude Code skills, mods, and catalogues. Install a resource here once, then link or copy only the skills a project needs.

```
resources/
├── README.md                  this file
├── resources.json             manifest: every resource, its source, license, and review status
├── skills/                    installable skills, vendored verbatim, grouped by category
│   ├── design/
│   │   ├── ui-ux-pro-max/     (ui-ux-pro-max, design)          MIT
│   │   └── design-md/         (design-md)                       Apache-2.0
│   ├── frontend/
│   │   └── frontend-design/   (frontend-design)                 Apache-2.0
│   ├── motion/
│   │   ├── emil-design-eng/   (8 motion skills)                 MIT
│   │   └── design-motion-principles/                           MIT
│   └── threejs/
│       └── cesartevisual-threejs-skills/  (24 skills)          MIT
├── mods/                      mod guides and notes. Nothing here is installed.
├── catalogues/                discovery lists and comparisons, plus external sources
├── docs/
│   └── SECURITY-REVIEW.md     review record and held decisions
└── scripts/
    ├── setup-project.sh       entry point: list, install, uninstall, validate
    ├── library.py             the engine (Python 3 stdlib only)
    └── tests/test_library.py  end-to-end tests
```

Each vendored collection has a `LICENSE` and a `SOURCE.md` with the repo URL, pinned commit, and what was copied.

## Quick start

```bash
scripts/setup-project.sh --list                                  # browse skills and presets
scripts/setup-project.sh ~/projects/portfolio --preset portfolio --dry-run
scripts/setup-project.sh ~/projects/portfolio --preset portfolio # links into .claude/skills/
scripts/setup-project.sh ~/projects/portfolio --skills threejs-audio,animate --mode copy
scripts/setup-project.sh ~/projects/portfolio --uninstall --dry-run
scripts/setup-project.sh --validate                              # check the library
```

Run `scripts/setup-project.sh <project>` with no selection in a terminal to choose skills interactively.

## Presets

| Preset | Skills | For |
|---|---|---|
| `portfolio` | 30: 20 Three.js, `frontend-design`, `ui-ux-pro-max`, `design`, `design-md`, 6 motion | `~/projects/portfolio`, `~/projects/my-showcase` |
| `dashboard` | 6: `frontend-design`, `ui-ux-pro-max`, `design`, `design-md`, `animation-performance`, `review-animations` | `~/projects/alert-dashboard` |

Dashboards are data-first, so the dashboard preset has no 3D skills. For charts and data visualization, the platform's built-in `dataviz` skill is already available and is not duplicated here.

Presets are defined in `resources.json` under `presets`. Edit them there.

## What the installer does

- **Link (default):** creates `<project>/.claude/skills/<id>` as a symlink into this library. Updates here reach every linked project at once. Links use absolute paths, so do not commit them to a repo that other people clone. Use `--mode copy` for those.
- **Copy:** writes a full copy. Use it when the project must be portable.
- **Safety:** conflicts with anything it did not create (for example, a folder named `animate` you wrote yourself) abort the run before any change. It never touches `CLAUDE.md`, `settings*.json`, plugin configuration, or `~/.claude`.
- **Ledger:** writes `<project>/.claude/.resources-library.json` listing what it installed. Uninstall removes only those entries. A copy you have edited is kept, and so is a link that was replaced.
- **Verification:** after each install it checks that `SKILL.md` exists, that the frontmatter `name` matches the id, and that the file matches the manifest hash.

Verified in this environment: a test project where the installer created links for two Three.js skills was checked by asking Claude Code to list them, and it reported both with their exact descriptions. A hand-made copy and a hand-made symlink in a separate test project also loaded. The copy-mode installer path is covered by the unit tests, not by a live loader check.

## Browse the manifest

`resources.json` has one entry per resource:

- `kind`: `skill`, `catalogue`, `dependency`, `reference`, or `mod`
- `installable`, `status`: vendored, held, catalogue, app-dependency, platform-provided, or unreviewed
- `source`: repo, commit, commit date, upstream path
- `license`, `dependencies`, `installMethods`
- `securityReview`: status (`static-reviewed`, `needs-review`, `needs-decision`, `not-applicable`), date, and notes
- `skillMd.sha256`: hash of the vendored `SKILL.md`, checked by `--validate`

Held and catalogue items are described in [docs/SECURITY-REVIEW.md](docs/SECURITY-REVIEW.md) and [catalogues/sources.md](catalogues/sources.md).

## Add a skill

1. Copy the skill folder into `skills/<category>/<collection>/`. Keep upstream files unchanged.
2. Add the upstream `LICENSE` to the collection folder, and write a `SOURCE.md` with the repo, commit, and date.
3. Add an entry to `resources.json` with `kind: "skill"`, `installable: true`, `status: "vendored"`, `collection`, `path`, `source`, and `securityReview`. Set `skillMd.sha256` to `sha256sum <path>/SKILL.md`.
4. Add the id to a preset if it belongs in one.
5. Run `scripts/setup-project.sh --validate`, then `python3 -I -m unittest discover -s scripts/tests`.

Do not vendor `settings*.json`, `hooks.json`, `.mcp.json`, `plugin.json`, `.claude-plugin/`, or `.git/`. The validator rejects them.

## Update a skill

Vendored copies are verbatim and pinned. To update one:

1. Clone the new commit to a scratch directory. Read the diff and any new scripts before copying anything.
2. Replace the files in the library folder.
3. Update `source.commit` and `source.commitDate` in `resources.json` and in the collection's `SOURCE.md`.
4. Run `--validate`. It reports the changed hash; update `skillMd.sha256` to the new value.
5. Projects that link to the library pick up the change at once. Projects with copies need `--uninstall` and a reinstall.

## Remove a project-local install

```bash
scripts/setup-project.sh ~/projects/portfolio --uninstall --dry-run   # see what would be removed
scripts/setup-project.sh ~/projects/portfolio --uninstall            # remove, after confirmation
```

To remove one skill by hand, delete `<project>/.claude/skills/<id>` and its entry in `.claude/.resources-library.json`. Do not delete anything else in `.claude/skills/`, because it may be yours.

## Tests

```bash
python3 -I -m unittest discover -s scripts/tests -v
```

The 15 tests cover dry-run, link and copy installs, re-runs, conflicts, modified copies, protected project config, held and unknown ids, refusing to install into the library, and detection of a tampered skill. They use temporary projects and never touch a real project or `~/.claude`.

## Maintenance rules

- Nothing is installed globally. The library is the source of truth; projects get links or copies.
- Mods are never installed or enabled automatically. See [mods/README.md](mods/README.md).
- Held items need a decision before they are copied. Decisions and reasons are in [docs/SECURITY-REVIEW.md](docs/SECURITY-REVIEW.md).
- Licenses and notices stay with the code. Do not vendor a repo that has no license.
