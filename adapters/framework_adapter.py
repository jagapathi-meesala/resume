"""FrameworkAdapter: Generic wrapper for integrating AgentCore into external agent frameworks."""

from typing import Dict, Any
from core.agent_core import AgentCore


class FrameworkAdapter:
    """Provides standard interface for agent frameworks (e.g. LangChain, CrewAI, AutoGen wrappers)."""

    def __init__(self, agent_core: AgentCore = None):
        self.agent_core = agent_core or AgentCore()

    def execute_task(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Framework task execution entrypoint."""
        response = self.agent_core.process_request(task_input)
        return {
            "status": response.status,
            "agent_id": response.agent_id,
            "version": response.version,
            "output": response.result,
            "errors": response.errors,
            "summary": response.execution_summary
        }
