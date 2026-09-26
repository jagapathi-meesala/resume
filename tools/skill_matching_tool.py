"""Skill Matching Tool: Perform explainable skill comparison between candidate skills and job demands."""

import time
from typing import Dict, Any, List
from contracts.tool_contract import BaseTool, ToolResult
from config.settings import MatchingSettings


class SkillMatchingTool(BaseTool):
    def __init__(self, settings: MatchingSettings = None):
        super().__init__(
            name="skill_matching_tool",
            description="Compares candidate skills from resume against job description requirements to produce explainable match classifications.",
            capability="skill_matching"
        )
        self.settings = settings or MatchingSettings.load_from_json()

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        return "resume_profile" in input_data and "job_profile" in input_data

    def run(self, input_data: Dict[str, Any]) -> ToolResult:
        start_time = time.time()
        resume_profile = input_data["resume_profile"]
        job_profile = input_data["job_profile"]

        resume_skills = set(s.lower() for s in resume_profile.get("skills", []))
        req_skills = set(s.lower() for s in job_profile.get("required_skills", []))
        pref_skills = set(s.lower() for s in job_profile.get("preferred_skills", []))

        matched_skills: List[Dict[str, Any]] = []
        partially_matched_skills: List[Dict[str, Any]] = []
        missing_skills: List[Dict[str, Any]] = []

        # Check required skills
        for req in req_skills:
            canonical_req = self.settings.skill_aliases.get(req, req)
            if canonical_req in resume_skills or req in resume_skills:
                matched_skills.append({
                    "skill": req,
                    "requirement_type": "required",
                    "match_type": "matched",
                    "resume_evidence": f"Explicitly listed in resume under skills as '{req}'",
                    "job_requirement": f"Required by job description"
                })
            else:
                # Check partial substring or category match
                partial_found = False
                for r_skill in resume_skills:
                    if req in r_skill or r_skill in req:
                        partially_matched_skills.append({
                            "skill": req,
                            "related_resume_skill": r_skill,
                            "requirement_type": "required",
                            "match_type": "partially_matched",
                            "resume_evidence": f"Related skill '{r_skill}' listed in resume",
                            "job_requirement": f"Required skill '{req}'"
                        })
                        partial_found = True
                        break
                if not partial_found:
                    missing_skills.append({
                        "skill": req,
                        "requirement_type": "required",
                        "match_type": "missing",
                        "job_requirement": f"Required skill '{req}'",
                        "reason": "No sufficiently matching resume evidence found"
                    })

        # Check preferred skills
        for pref in pref_skills:
            canonical_pref = self.settings.skill_aliases.get(pref, pref)
            if canonical_pref in resume_skills or pref in resume_skills:
                matched_skills.append({
                    "skill": pref,
                    "requirement_type": "preferred",
                    "match_type": "matched",
                    "resume_evidence": f"Listed in resume as '{pref}'",
                    "job_requirement": f"Preferred by job description"
                })
            else:
                missing_skills.append({
                    "skill": pref,
                    "requirement_type": "preferred",
                    "match_type": "missing",
                    "job_requirement": f"Preferred skill '{pref}'",
                    "reason": "Optional skill not explicitly stated in resume"
                })

        elapsed = (time.time() - start_time) * 1000
        return ToolResult(
            success=True,
            data={
                "matched_skills": matched_skills,
                "partially_matched_skills": partially_matched_skills,
                "missing_skills": missing_skills,
                "summary": {
                    "total_job_skills": len(req_skills) + len(pref_skills),
                    "matched_count": len(matched_skills),
                    "partially_matched_count": len(partially_matched_skills),
                    "missing_count": len(missing_skills)
                }
            },
            execution_time_ms=elapsed
        )
