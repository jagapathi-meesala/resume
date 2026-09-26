"""PortableAdapter: Framework-independent entry point for agent execution."""

from typing import Dict, Any
from core.agent_core import AgentCore
from contracts.agent_contract import AgentResponse


class PortableAdapter:
    """Portable adapter allowing execution in any Python environment without external frameworks."""

    def __init__(self, agent_core: AgentCore = None):
        self.agent_core = agent_core or AgentCore()

    def run(self, resume: Any, job_description: Any, configuration: Dict[str, Any] = None) -> AgentResponse:
        request_payload = {
            "resume": resume,
            "job_description": job_description,
            "configuration": configuration or {}
        }
        return self.agent_core.process_request(request_payload)
