"""Multi-agent adapters package for Essentials."""

from adapters.base import BaseAdapter
from adapters.registry import get_adapter, list_adapters, supported_agent_names

__all__ = ["BaseAdapter", "get_adapter", "list_adapters", "supported_agent_names"]

