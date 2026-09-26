"""AgentCore: Single source of truth for request processing, capability verification, and lifecycle management."""

import uuid
from typing import Dict, Any, Optional, List
from passport.passport_manager import PassportManager
from registry.tool_registry import ToolRegistry
from core.execution_engine import ExecutionEngine
from core.state_manager import StateManager
from core.validators import RequestValidator, PrivacyRedactor
from contracts.agent_contract import AgentRequest, AgentResponse
from contracts.behavior_contract import LifecyclePhase, BehaviorContract, PROTECTED_CHARACTERISTICS

# Register default tools
from tools.resume_profiler_tool import ResumeProfilerTool
from tools.job_description_profiler_tool import JobDescriptionProfilerTool
from tools.skill_matching_tool import SkillMatchingTool
from tools.qualification_gap_tool import QualificationGapTool
from tools.compatibility_analyzer_tool import CompatibilityAnalyzerTool
from tools.recommendation_tool import RecommendationTool
from tools.matching_report_tool import MatchingReportTool


class AgentCore:
    """Core framework-independent controller for Resume & Job Matching Agent."""

    def __init__(self, passport_manager: Optional[PassportManager] = None, registry: Optional[ToolRegistry] = None):
        self.passport_manager = passport_manager or PassportManager()
        self.registry = registry or ToolRegistry()
        self._initialize_default_tools()
        self.execution_engine = ExecutionEngine(self.registry)
        self.passport = self.passport_manager.get_passport()

    def _initialize_default_tools(self) -> None:
        """Register domain tools dynamically if not already registered."""
        tools_to_register = [
            ResumeProfilerTool(),
            JobDescriptionProfilerTool(),
            SkillMatchingTool(),
            QualificationGapTool(),
            CompatibilityAnalyzerTool(),
            RecommendationTool(),
            MatchingReportTool()
        ]
        for tool in tools_to_register:
            if not self.registry.get_tool(tool.name):
                self.registry.register_tool(tool)

    def process_request(self, request_payload: Dict[str, Any]) -> AgentResponse:
        request_id = str(uuid.uuid4())
        state = StateManager(request_id)
        errors: List[str] = []

        try:
            # Phase 1: INPUT & REQUEST_VALIDATION
            state.transition_to(LifecyclePhase.INPUT)
            state.transition_to(LifecyclePhase.REQUEST_VALIDATION)
            is_valid, err_msg = RequestValidator.validate_request(request_payload)
            if not is_valid:
                return AgentResponse(
                    request_id=request_id,
                    status="FAILED",
                    agent_id=self.passport.agent_id,
                    version=self.passport.version,
                    result={},
                    errors=[PrivacyRedactor.sanitize_text(err_msg)],
                    execution_summary=state.get_execution_summary()
                )

            # Check non-discrimination constraint
            resume_text = str(request_payload.get("resume", ""))
            jd_text = str(request_payload.get("job_description", ""))
            BehaviorContract.validate_non_discrimination(resume_text + " " + jd_text)

            # Phase 2: PASSPORT_LOADING
            state.transition_to(LifecyclePhase.PASSPORT_LOADING)
            passport = self.passport_manager.get_passport()

            # Phase 3: CAPABILITY_VALIDATION
            state.transition_to(LifecyclePhase.CAPABILITY_VALIDATION)
            declared_caps = set(self.passport_manager.get_declared_capabilities())
            registered_caps = set(self.registry.list_capabilities())
            missing_caps = declared_caps - registered_caps
            if missing_caps:
                errors.append(f"Missing implementation for declared capabilities: {missing_caps}")

            # Phase 4: TOOL_DISCOVERY
            state.transition_to(LifecyclePhase.TOOL_DISCOVERY)
            discovered_tools = self.registry.list_tools()
            state.set_context("discovered_tools", discovered_tools)

            # Phase 5-12: PIPELINE EXECUTION
            final_report = self.execution_engine.execute_pipeline(request_payload, state)

            # Phase 13: RESULT_VALIDATION
            state.transition_to(LifecyclePhase.RESULT_VALIDATION)

            # Phase 14: RESPONSE_GENERATION
            state.transition_to(LifecyclePhase.RESPONSE_GENERATION)

            return AgentResponse(
                request_id=request_id,
                status="SUCCESS",
                agent_id=passport.agent_id,
                version=passport.version,
                result=final_report,
                errors=errors,
                execution_summary=state.get_execution_summary()
            )

        except Exception as e:
            sanitized_err = PrivacyRedactor.sanitize_text(str(e))
            return AgentResponse(
                request_id=request_id,
                status="FAILED",
                agent_id=self.passport.agent_id,
                version=self.passport.version,
                result={},
                errors=[sanitized_err],
                execution_summary=state.get_execution_summary()
            )
