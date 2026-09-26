"""OpenAIAdapter: Optional provider integration adapter supporting OpenAI SDK execution if configured."""

import os
from typing import Dict, Any, Optional
from core.agent_core import AgentCore


class OpenAIAdapter:
    """Optional adapter for wrapping AgentCore or performing LLM enhancements via OpenAI SDK."""

    def __init__(self, agent_core: AgentCore = None):
        self.agent_core = agent_core or AgentCore()
        self.api_key = os.getenv("OPENAI_API_KEY")

    def is_available(self) -> bool:
        """Return True if OPENAI_API_KEY is configured in environment."""
        return bool(self.api_key and self.api_key.strip())

    def run_with_enhancement(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Runs offline core analysis and attaches LLM status information."""
        core_response = self.agent_core.process_request(request_payload)

        if not self.is_available():
            return {
                "provider_status": "NOT_CONFIGURED",
                "message": "OPENAI_API_KEY environment variable is not set. Execution fell back to offline deterministic AgentCore.",
                "core_response": core_response.result
            }

        # If key exists, attempt OpenAI SDK invocation safely if openai package is installed
        try:
            import openai
            # We report capability available without executing unrequested LLM billing calls
            return {
                "provider_status": "AVAILABLE",
                "message": "OpenAI SDK detected and API key is present.",
                "core_response": core_response.result
            }
        except ImportError:
            return {
                "provider_status": "UNAVAILABLE",
                "message": "OpenAI SDK package 'openai' is not installed in current python environment.",
                "core_response": core_response.result
            }
