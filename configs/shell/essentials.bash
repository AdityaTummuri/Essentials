# Essentials shell enhancements for Bash
# Source in ~/.bashrc:
#   [ -f /path/to/Essentials/configs/shell/essentials.bash ] && source /path/to/Essentials/configs/shell/essentials.bash

# Safe navigation and directory shortcuts
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Colorized, readable listing
if ls --color=auto >/dev/null 2>&1; then
    alias ls='ls --color=auto'
    alias ll='ls -lh --color=auto'
    alias la='ls -lah --color=auto'
fi

# Git shortcuts
alias g='git'
alias gst='git status -sb'
alias gco='git checkout'
alias gbr='git branch'
alias glg='git log --oneline -n 15'
alias gd='git diff'

# Python shortcuts
alias py='python3'
alias venv-activate='[ -f .venv/bin/activate ] && source .venv/bin/activate || echo "No .venv/bin/activate found"'
alias pyclean='find . -type d -name __pycache__ -exec rm -rf {} +; find . -type f -name "*.py[co]" -delete'

# Modern safety guards
alias cp='cp -i'
alias mv='mv -i'
