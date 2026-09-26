"""Passport contract definitions."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class CapabilityDeclaration:
    name: str
    description: str
    tool: str


@dataclass
class PassportData:
    agent_id: str
    name: str
    display_name: str
    version: str
    description: str
    author: str
    license: str
    capabilities: List[CapabilityDeclaration] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    lifecycle_phases: List[str] = field(default_factory=list)
    verification_status: Dict[str, Any] = field(default_factory=dict)
