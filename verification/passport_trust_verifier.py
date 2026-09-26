"""Passport Trust Verifier: Dynamically inspects agent passport and matches declarations against ToolRegistry."""

from typing import Dict, Any
from passport.passport_manager import PassportManager
from registry.tool_registry import ToolRegistry
from tools.resume_profiler_tool import ResumeProfilerTool
from tools.job_description_profiler_tool import JobDescriptionProfilerTool
from tools.skill_matching_tool import SkillMatchingTool
from tools.qualification_gap_tool import QualificationGapTool
from tools.compatibility_analyzer_tool import CompatibilityAnalyzerTool
from tools.recommendation_tool import RecommendationTool
from tools.matching_report_tool import MatchingReportTool


class PassportTrustVerifier:
    def __init__(self, passport_manager: PassportManager = None, registry: ToolRegistry = None):
        self.passport_manager = passport_manager or PassportManager()
        if registry is None:
            self.registry = ToolRegistry()
            # Register tools
            self.registry.register_tool(ResumeProfilerTool())
            self.registry.register_tool(JobDescriptionProfilerTool())
            self.registry.register_tool(SkillMatchingTool())
            self.registry.register_tool(QualificationGapTool())
            self.registry.register_tool(CompatibilityAnalyzerTool())
            self.registry.register_tool(RecommendationTool())
            self.registry.register_tool(MatchingReportTool())
        else:
            self.registry = registry

    def verify(self) -> Dict[str, Any]:
        """Perform dynamic verification of agent passport integrity."""
        errors = []
        warnings = []

        try:
            passport = self.passport_manager.get_passport()
            self.passport_manager.validate_schema()
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"Passport load/schema verification failed: {str(e)}",
                "details": {}
            }

        # Dynamic discovery
        declared_tools = set(self.passport_manager.get_declared_tools())
        registered_tools = set(self.registry.list_tools())

        declared_caps = set(self.passport_manager.get_declared_capabilities())
        registered_caps = set(self.registry.list_capabilities())

        missing_tools = declared_tools - registered_tools
        extra_tools = registered_tools - declared_tools

        missing_caps = declared_caps - registered_caps
        extra_caps = registered_caps - declared_caps

        if missing_tools:
            errors.append(f"Passport declares tools not present in ToolRegistry: {missing_tools}")
        if missing_caps:
            errors.append(f"Passport declares capabilities not registered: {missing_caps}")

        if extra_tools:
            warnings.append(f"ToolRegistry has extra tools not declared in passport: {extra_tools}")
        if extra_caps:
            warnings.append(f"ToolRegistry has extra capabilities not declared in passport: {extra_caps}")

        status = "PASS" if not errors else "FAIL"
        return {
            "status": status,
            "message": "Passport trust verification completed.",
            "details": {
                "agent_id": passport.agent_id,
                "declared_tools_count": len(declared_tools),
                "registered_tools_count": len(registered_tools),
                "declared_capabilities_count": len(declared_caps),
                "registered_capabilities_count": len(registered_caps),
                "errors": errors,
                "warnings": warnings
            }
        }
