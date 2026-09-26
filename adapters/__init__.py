"""Adapters package for framework integration and portability."""

from adapters.portable_adapter import PortableAdapter
from adapters.framework_adapter import FrameworkAdapter
from adapters.openai_adapter import OpenAIAdapter

__all__ = [
    "PortableAdapter",
    "FrameworkAdapter",
    "OpenAIAdapter"
]
