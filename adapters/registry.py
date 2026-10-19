"""Adapter registry for discovering and resolving agent adapters."""

from __future__ import annotations

from typing import Dict, List, Optional
from adapters.base import BaseAdapter
from adapters.claude_code import ClaudeCodeAdapter
from adapters.gemini_cli import GeminiCliAdapter
from adapters.codex import CodexAdapter
from adapters.cursor import CursorAdapter
from adapters.windsurf import WindsurfAdapter
from adapters.copilot import CopilotAdapter
from adapters.opencode import OpenCodeAdapter

_ADAPTERS: list[BaseAdapter] = [
    ClaudeCodeAdapter(),
    GeminiCliAdapter(),
    CodexAdapter(),
    CursorAdapter(),
    WindsurfAdapter(),
    CopilotAdapter(),
    OpenCodeAdapter(),
]

_LOOKUP: dict[str, BaseAdapter] = {}
for adapter in _ADAPTERS:
    _LOOKUP[adapter.name.lower()] = adapter
    for alias in adapter.aliases:
        _LOOKUP[alias.lower()] = adapter


def get_adapter(name_or_alias: str) -> BaseAdapter:
    """Resolve an adapter by name or alias, raising ValueError if not found."""
    cleaned = name_or_alias.strip().lower()
    if cleaned in _LOOKUP:
        return _LOOKUP[cleaned]
    known = sorted(list({a.name for a in _ADAPTERS}))
    raise ValueError(f"Unknown agent '{name_or_alias}'. Supported agents: {', '.join(known)}")


def list_adapters() -> list[BaseAdapter]:
    """Return all registered agent adapters."""
    return list(_ADAPTERS)


def supported_agent_names() -> list[str]:
    """Return unique primary names of all supported agents."""
    return [a.name for a in _ADAPTERS]

