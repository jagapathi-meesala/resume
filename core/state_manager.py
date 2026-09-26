"""StateManager tracks step-by-step lifecycle state during execution."""

from typing import Dict, Any, List, Optional
from contracts.behavior_contract import LifecyclePhase


class StateManager:
    def __init__(self, request_id: str):
        self.request_id = request_id
        self.current_phase: Optional[str] = None
        self.phase_history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}

    def transition_to(self, phase: LifecyclePhase, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.current_phase = phase.value
        entry = {
            "phase": phase.value,
            "metadata": metadata or {}
        }
        self.phase_history.append(entry)

    def set_context(self, key: str, value: Any) -> None:
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        return self.context.get(key, default)

    def get_execution_summary(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "completed_phases": [entry["phase"] for entry in self.phase_history],
            "total_phases_executed": len(self.phase_history)
        }
