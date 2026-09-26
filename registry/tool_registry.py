"""ToolRegistry handles registration, lookup, and dynamic capability discovery of tools."""

from typing import Dict, Any, List, Optional
from contracts.tool_contract import BaseTool, ToolResult


class ToolRegistry:
    """Dynamic tool registry for Resume & Job Matching Agent."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._capabilities: Dict[str, str] = {}  # capability_name -> tool_name

    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool instance dynamically."""
        if not isinstance(tool, BaseTool):
            raise TypeError(f"Tool must inherit from BaseTool, got {type(tool)}")

        self._tools[tool.name] = tool
        self._capabilities[tool.capability] = tool.name

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Retrieve a tool by name."""
        return self._tools.get(name)

    def get_tool_for_capability(self, capability: str) -> Optional[BaseTool]:
        """Retrieve tool associated with a capability."""
        tool_name = self._capabilities.get(capability)
        if tool_name:
            return self._tools.get(tool_name)
        return None

    def list_tools(self) -> List[str]:
        """Return list of registered tool names."""
        return list(self._tools.keys())

    def list_capabilities(self) -> List[str]:
        """Return list of supported capabilities."""
        return list(self._capabilities.keys())

    def get_all_metadata(self) -> List[Dict[str, Any]]:
        """Return metadata for all registered tools."""
        return [tool.get_metadata() for tool in self._tools.values()]

    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> ToolResult:
        """Execute a tool by name with safety checks."""
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                data={},
                error=f"Tool '{tool_name}' not found in registry."
            )
        if not tool.validate_input(input_data):
            return ToolResult(
                success=False,
                data={},
                error=f"Invalid input schema for tool '{tool_name}'."
            )
        return tool.run(input_data)
