"""Tool contract definitions for all domain tools."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class ToolResult:
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class BaseTool(ABC):
    """Abstract Base Class for all Resume & Job Matching Agent tools."""

    def __init__(self, name: str, description: str, capability: str):
        self.name = name
        self.description = description
        self.capability = capability

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input dictionary according to tool schema."""
        pass

    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> ToolResult:
        """Execute tool logic and return structured ToolResult."""
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata describing the tool."""
        return {
            "name": self.name,
            "description": self.description,
            "capability": self.capability
        }
