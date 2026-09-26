"""ProviderBoundary isolates optional external AI model providers from AgentCore."""

import os
from enum import Enum
from typing import Dict, Any, Optional


class ProviderStatus(str, Enum):
    NOT_CONFIGURED = "PROVIDER_NOT_CONFIGURED"
    UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    AUTH_FAILED = "PROVIDER_AUTH_FAILED"
    REQUEST_FAILED = "PROVIDER_REQUEST_FAILED"
    SUCCESS = "PROVIDER_SUCCESS"


class ProviderBoundary:
    """Manages external provider state, credential verification, and structured status reports."""

    def __init__(self, provider_name: str = "openai"):
        self.provider_name = provider_name

    def check_status(self) -> Dict[str, Any]:
        """Check provider configuration without leaking secrets."""
        if self.provider_name == "openai":
            key = os.getenv("OPENAI_API_KEY")
            if not key or not key.strip():
                return {
                    "status": ProviderStatus.NOT_CONFIGURED.value,
                    "provider": self.provider_name,
                    "message": "OPENAI_API_KEY is not set in environment."
                }
            try:
                import openai
                return {
                    "status": ProviderStatus.SUCCESS.value,
                    "provider": self.provider_name,
                    "message": "OpenAI SDK is available and credentials are configured."
                }
            except ImportError:
                return {
                    "status": ProviderStatus.UNAVAILABLE.value,
                    "provider": self.provider_name,
                    "message": "OpenAI Python library is not installed."
                }
        return {
            "status": ProviderStatus.NOT_CONFIGURED.value,
            "provider": self.provider_name,
            "message": f"Provider '{self.provider_name}' is not configured."
        }
