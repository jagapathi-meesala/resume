"""Agent contract specifying input request and response models."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class AgentRequest:
    resume: Any  # Union[str, Dict[str, Any]]
    job_description: Any  # Union[str, Dict[str, Any]]
    configuration: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


@dataclass
class AgentResponse:
    request_id: str
    status: str  # "SUCCESS", "PARTIAL_SUCCESS", "FAILED"
    agent_id: str
    version: str
    result: Dict[str, Any]
    errors: List[str] = field(default_factory=list)
    execution_summary: Dict[str, Any] = field(default_factory=dict)
