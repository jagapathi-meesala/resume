"""Qualification Gap Tool: Identifies missing skills, experience gaps, and education differences."""

import time
from typing import Dict, Any, List
from contracts.tool_contract import BaseTool, ToolResult


class QualificationGapTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="qualification_gap_tool",
            description="Analyzes differences between candidate profile and job requirements to pinpoint actionable qualification gaps.",
            capability="qualification_gap_analysis"
        )

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        return "skill_matching_result" in input_data and "resume_profile" in input_data and "job_profile" in input_data

    def run(self, input_data: Dict[str, Any]) -> ToolResult:
        start_time = time.time()
        skill_match = input_data["skill_matching_result"]
        resume_profile = input_data["resume_profile"]
        job_profile = input_data["job_profile"]

        gaps: List[Dict[str, Any]] = []

        # 1. Missing Required Skills
        for item in skill_match.get("missing_skills", []):
            if item.get("requirement_type") == "required":
                gaps.append({
                    "category": "required_skill",
                    "item": item["skill"],
                    "severity": "HIGH",
                    "description": f"Missing required core skill '{item['skill']}' in candidate profile."
                })

        # 2. Missing Preferred Skills
        for item in skill_match.get("missing_skills", []):
            if item.get("requirement_type") == "preferred":
                gaps.append({
                    "category": "preferred_skill",
                    "item": item["skill"],
                    "severity": "MEDIUM",
                    "description": f"Candidate does not explicitly mention preferred skill '{item['skill']}'."
                })

        # 3. Education Gaps
        req_edu = job_profile.get("education_requirements", [])
        res_edu = resume_profile.get("education", [])
        if req_edu and not res_edu:
            gaps.append({
                "category": "education",
                "item": ", ".join(req_edu),
                "severity": "MEDIUM",
                "description": f"Job specifies {', '.join(req_edu)} but no formal education degree was extracted from resume."
            })

        # 4. Experience Gaps
        req_exp = job_profile.get("experience_requirements", [])
        res_exp = resume_profile.get("experience", [])
        if req_exp and not res_exp:
            gaps.append({
                "category": "experience",
                "item": ", ".join(req_exp),
                "severity": "MEDIUM",
                "description": f"Job specifies experience expectations ({', '.join(req_exp)}) but candidate experience metrics were unquantified."
            })

        elapsed = (time.time() - start_time) * 1000
        return ToolResult(
            success=True,
            data={
                "gaps": gaps,
                "gap_summary": {
                    "total_gaps": len(gaps),
                    "high_severity": sum(1 for g in gaps if g["severity"] == "HIGH"),
                    "medium_severity": sum(1 for g in gaps if g["severity"] == "MEDIUM")
                }
            },
            execution_time_ms=elapsed
        )
