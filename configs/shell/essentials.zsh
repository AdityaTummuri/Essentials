# Essentials shell enhancements for Zsh
# Source in ~/.zshrc:
#   [ -f /path/to/Essentials/configs/shell/essentials.zsh ] && source /path/to/Essentials/configs/shell/essentials.zsh

# Directory navigation
setopt AUTO_CD
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS

# History configuration
HISTSIZE=50000
SAVEHIST=50000
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_VERIFY
setopt SHARE_HISTORY

# Aliases
alias ..='cd ..'
alias ...='cd ../..'
alias g='git'
alias gst='git status -sb'
alias gco='git checkout'
alias gbr='git branch'
alias glg='git log --oneline -n 15'
alias gd='git diff'
alias py='python3'
alias venv-activate='[ -f .venv/bin/activate ] && source .venv/bin/activate || echo "No .venv/bin/activate found"'
alias pyclean='find . -type d -name __pycache__ -exec rm -rf {} +; find . -type f -name "*.py[co]" -delete'
