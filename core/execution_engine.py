"""ExecutionEngine orchestrates tool execution pipeline for job matching analysis."""

import uuid
from typing import Dict, Any, List
from registry.tool_registry import ToolRegistry
from core.state_manager import StateManager
from contracts.behavior_contract import LifecyclePhase


class ExecutionEngine:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute_pipeline(self, request_payload: Dict[str, Any], state: StateManager) -> Dict[str, Any]:
        """Runs the complete analysis pipeline step-by-step through registered tools."""

        # Phase: RESUME_PROFILING
        state.transition_to(LifecyclePhase.RESUME_PROFILING)
        resume_res = self.registry.execute_tool("resume_profiler_tool", {"resume": request_payload["resume"]})
        if not resume_res.success:
            raise RuntimeError(f"Resume profiling failed: {resume_res.error}")
        resume_profile = resume_res.data["resume_profile"]
        state.set_context("resume_profile", resume_profile)

        # Phase: JOB_PROFILING
        state.transition_to(LifecyclePhase.JOB_PROFILING)
        job_res = self.registry.execute_tool("job_description_profiler_tool", {"job_description": request_payload["job_description"]})
        if not job_res.success:
            raise RuntimeError(f"Job description profiling failed: {job_res.error}")
        job_profile = job_res.data["job_profile"]
        state.set_context("job_profile", job_profile)

        # Phase: SKILL_MATCHING
        state.transition_to(LifecyclePhase.SKILL_MATCHING)
        match_res = self.registry.execute_tool("skill_matching_tool", {
            "resume_profile": resume_profile,
            "job_profile": job_profile
        })
        if not match_res.success:
            raise RuntimeError(f"Skill matching failed: {match_res.error}")
        skill_matching_result = match_res.data
        state.set_context("skill_matching_result", skill_matching_result)

        # Phase: GAP_ANALYSIS
        state.transition_to(LifecyclePhase.GAP_ANALYSIS)
        gap_res = self.registry.execute_tool("qualification_gap_tool", {
            "skill_matching_result": skill_matching_result,
            "resume_profile": resume_profile,
            "job_profile": job_profile
        })
        if not gap_res.success:
            raise RuntimeError(f"Gap analysis failed: {gap_res.error}")
        gap_result = gap_res.data
        state.set_context("gap_analysis_result", gap_result)

        # Phase: COMPATIBILITY_ANALYSIS
        state.transition_to(LifecyclePhase.COMPATIBILITY_ANALYSIS)
        compat_res = self.registry.execute_tool("compatibility_analyzer_tool", {
            "skill_matching_result": skill_matching_result,
            "gap_analysis_result": gap_result
        })
        if not compat_res.success:
            raise RuntimeError(f"Compatibility analysis failed: {compat_res.error}")
        compatibility_result = compat_res.data
        state.set_context("compatibility_result", compatibility_result)

        # Phase: RECOMMENDATION_GENERATION
        state.transition_to(LifecyclePhase.RECOMMENDATION_GENERATION)
        rec_res = self.registry.execute_tool("recommendation_tool", {
            "skill_matching_result": skill_matching_result,
            "gap_analysis_result": gap_result
        })
        if not rec_res.success:
            raise RuntimeError(f"Recommendation generation failed: {rec_res.error}")
        recommendations_result = rec_res.data
        state.set_context("recommendations_result", recommendations_result)

        # Phase: REPORT_GENERATION
        state.transition_to(LifecyclePhase.REPORT_GENERATION)
        report_res = self.registry.execute_tool("matching_report_tool", {
            "resume_profile": resume_profile,
            "job_profile": job_profile,
            "skill_matching_result": skill_matching_result,
            "gap_analysis_result": gap_result,
            "compatibility_result": compatibility_result,
            "recommendations_result": recommendations_result
        })
        if not report_res.success:
            raise RuntimeError(f"Report generation failed: {report_res.error}")
        final_report = report_res.data["matching_report"]
        state.set_context("matching_report", final_report)

        return final_report
