"""Matching Report Tool: Assembles comprehensive structured analysis reports."""

import time
from typing import Dict, Any
from contracts.tool_contract import BaseTool, ToolResult


class MatchingReportTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="matching_report_tool",
            description="Compiles extracted profiles, skill matches, qualification gaps, compatibility score, and recommendations into a unified structured report.",
            capability="matching_report"
        )

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        required_keys = [
            "resume_profile", "job_profile", "skill_matching_result",
            "gap_analysis_result", "compatibility_result", "recommendations_result"
        ]
        return all(key in input_data for key in required_keys)

    def run(self, input_data: Dict[str, Any]) -> ToolResult:
        start_time = time.time()

        resume_profile = input_data["resume_profile"]
        job_profile = input_data["job_profile"]
        skill_match = input_data["skill_matching_result"]
        gap_analysis = input_data["gap_analysis_result"]
        compatibility = input_data["compatibility_result"]
        recommendations = input_data["recommendations_result"]

        report = {
            "report_header": {
                "agent_name": "resume-job-matching-agent",
                "version": "1.0.0",
                "analysis_type": "Deterministic Offline Job Match Analysis"
            },
            "provenance_summary": {
                "resume_input_length": resume_profile.get("raw_text_length", 0),
                "skills_extracted_count": len(resume_profile.get("skills", [])),
                "job_requirements_count": len(job_profile.get("job_relevant_keywords", []))
            },
            "resume_profile": resume_profile,
            "job_profile": job_profile,
            "skill_matching": {
                "matched_skills": skill_match.get("matched_skills", []),
                "partially_matched_skills": skill_match.get("partially_matched_skills", []),
                "missing_skills": skill_match.get("missing_skills", []),
                "summary": skill_match.get("summary", {})
            },
            "qualification_gaps": gap_analysis,
            "compatibility_analysis": compatibility,
            "recommendations": recommendations.get("recommendations", []),
            "limitations_and_disclaimer": [
                "Analysis relies strictly on explicit evidence in supplied input documents.",
                "Non-job protected characteristics (race, gender, age, disability, etc.) are excluded.",
                "Compatibility scores evaluate text & skill alignment only and DO NOT predict hiring outcomes.",
                "The agent acts as an analytical assistant, not an autonomous hiring decision maker."
            ]
        }

        elapsed = (time.time() - start_time) * 1000
        return ToolResult(
            success=True,
            data={"matching_report": report},
            execution_time_ms=elapsed
        )
