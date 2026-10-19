# Developer Environment Configurations

Essentials provides modular, safe, and transparent environment configurations for developer machines.

## Safety Principles

1. **Explicit Opt-in Only**: Configurations in this directory are never automatically installed into your home directory or global system files.
2. **Non-Destructive**: They are provided as modular templates designed to be inspected, copied, or sourced.
3. **No Lock-in**: All configurations use standard open configuration formats without proprietary tooling requirements.

## Available Configurations

| Category | File | Description | Usage |
|---|---|---|---|
| **Editor** | `editor/.editorconfig` | Universal formatting rules (2-space web, 4-space python, utf-8, lf) | Copy to project root: `cp configs/editor/.editorconfig ~/projects/my-project/` |
| **Git** | `git/.gitconfig.template` | Recommended Git defaults (pull.rebase, histogram diff, useful aliases) | Inspect and merge into `~/.gitconfig` or project `.git/config` |
| **Git** | `git/.gitignore.template` | Multi-language, security-conscious gitignore | Copy or append to project `.gitignore` |
| **Shell** | `shell/essentials.bash` | Modular, safe bash aliases and navigation shortcuts | Source in `~/.bashrc`: `source /path/to/configs/shell/essentials.bash` |
| **Shell** | `shell/essentials.zsh` | Zsh history, auto-cd, and workflow aliases | Source in `~/.zshrc`: `source /path/to/configs/shell/essentials.zsh` |
