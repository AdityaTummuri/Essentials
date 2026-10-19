#!/usr/bin/env bash
# Install selected Claude Code skills from this library into a project.
#
#   scripts/setup-project.sh ~/projects/portfolio --preset portfolio --dry-run
#   scripts/setup-project.sh ~/projects/portfolio --skills threejs-scene,animate --mode copy
#   scripts/setup-project.sh ~/projects/portfolio --uninstall
#   scripts/setup-project.sh --list
#   scripts/setup-project.sh --validate
#
# Run with no selection in a terminal to pick skills interactively.
# Options and behaviour are documented in README.md and in library.py.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is required" >&2
  exit 2
fi

# -I: isolated mode. Ignores PYTHON* environment variables and the current directory on sys.path.
exec python3 -I "$here/library.py" "$@"
