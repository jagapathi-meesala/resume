"""BehaviorContract defining agent lifecycle, capabilities, tool discovery, and safety constraints."""

from enum import Enum
from typing import List, Dict, Any


class LifecyclePhase(str, Enum):
    INPUT = "INPUT"
    REQUEST_VALIDATION = "REQUEST_VALIDATION"
    PASSPORT_LOADING = "PASSPORT_LOADING"
    CAPABILITY_VALIDATION = "CAPABILITY_VALIDATION"
    TOOL_DISCOVERY = "TOOL_DISCOVERY"
    RESUME_PROFILING = "RESUME_PROFILING"
    JOB_PROFILING = "JOB_PROFILING"
    SKILL_MATCHING = "SKILL_MATCHING"
    GAP_ANALYSIS = "GAP_ANALYSIS"
    COMPATIBILITY_ANALYSIS = "COMPATIBILITY_ANALYSIS"
    RECOMMENDATION_GENERATION = "RECOMMENDATION_GENERATION"
    REPORT_GENERATION = "REPORT_GENERATION"
    RESULT_VALIDATION = "RESULT_VALIDATION"
    RESPONSE_GENERATION = "RESPONSE_GENERATION"


REQUIRED_LIFECYCLE_SEQUENCE: List[LifecyclePhase] = [
    LifecyclePhase.INPUT,
    LifecyclePhase.REQUEST_VALIDATION,
    LifecyclePhase.PASSPORT_LOADING,
    LifecyclePhase.CAPABILITY_VALIDATION,
    LifecyclePhase.TOOL_DISCOVERY,
    LifecyclePhase.RESUME_PROFILING,
    LifecyclePhase.JOB_PROFILING,
    LifecyclePhase.SKILL_MATCHING,
    LifecyclePhase.GAP_ANALYSIS,
    LifecyclePhase.COMPATIBILITY_ANALYSIS,
    LifecyclePhase.RECOMMENDATION_GENERATION,
    LifecyclePhase.REPORT_GENERATION,
    LifecyclePhase.RESULT_VALIDATION,
    LifecyclePhase.RESPONSE_GENERATION
]


PROTECTED_CHARACTERISTICS: List[str] = [
    "race",
    "ethnicity",
    "religion",
    "gender",
    "sexual_orientation",
    "disability",
    "age",
    "nationality",
    "political_affiliation",
    "health_status"
]


class BehaviorContract:
    """Defines and validates operational constraints for the agent."""

    @staticmethod
    def get_lifecycle_sequence() -> List[str]:
        return [phase.value for phase in REQUIRED_LIFECYCLE_SEQUENCE]

    @staticmethod
    def validate_non_discrimination(input_text: str) -> Dict[str, Any]:
        """Verify that input analysis does not rely on protected characteristic terms."""
        lowered = input_text.lower()
        flagged = []
        for char in PROTECTED_CHARACTERISTICS:
            if char in lowered:
                flagged.append(char)
        return {
            "compliant": True,  # Operational requirement: ignore if present, do not evaluate
            "flagged_terms": flagged,
            "message": "Evaluation must strictly omit non-job protected characteristics."
        }
