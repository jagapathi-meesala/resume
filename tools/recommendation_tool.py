"""Recommendation Tool: Generates practical, evidence-based resume and candidate positioning suggestions."""

import time
from typing import Dict, Any, List
from contracts.tool_contract import BaseTool, ToolResult


class RecommendationTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="recommendation_tool",
            description="Generates actionable, evidence-based recommendations for resume optimization and skill development.",
            capability="recommendation_generation"
        )

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        return "skill_matching_result" in input_data and "gap_analysis_result" in input_data

    def run(self, input_data: Dict[str, Any]) -> ToolResult:
        start_time = time.time()
        skill_match = input_data["skill_matching_result"]
        gap_analysis = input_data["gap_analysis_result"]

        matched = skill_match.get("matched_skills", [])
        partially_matched = skill_match.get("partially_matched_skills", [])
        missing = skill_match.get("missing_skills", [])
        gaps = gap_analysis.get("gaps", [])

        recommendations: List[Dict[str, Any]] = []

        # 1. Skills to Highlight
        skills_to_highlight = [m["skill"] for m in matched if m.get("requirement_type") == "required"]
        if skills_to_highlight:
            recommendations.append({
                "category": "skills_to_highlight",
                "title": "Highlight Core Required Skills",
                "action": f"Emphasize existing verified skills ({', '.join(skills_to_highlight)}) prominently in the resume summary and bullet points.",
                "evidence": f"{len(skills_to_highlight)} required skills matched directly."
            })

        # 2. Missing Keywords to Address
        missing_req_keywords = [m["skill"] for m in missing if m.get("requirement_type") == "required"]
        if missing_req_keywords:
            recommendations.append({
                "category": "missing_keywords",
                "title": "Address Missing Job Keywords",
                "action": f"If candidate possesses hands-on experience with {', '.join(missing_req_keywords)}, explicitly add them to the skills section.",
                "evidence": f"Required job terms absent from resume text."
            })

        # 3. Partial Match Clarifications
        if partially_matched:
            partial_names = [p["skill"] for p in partially_matched]
            recommendations.append({
                "category": "weak_evidence",
                "title": "Clarify Related or Partial Skills",
                "action": f"Explicitly specify proficiency in {', '.join(partial_names)} rather than relying on related terms.",
                "evidence": f"Related skills were found but exact terminology differs."
            })

        # 4. Experience & Education Recommendations
        for gap in gaps:
            if gap["category"] in ("education", "experience"):
                recommendations.append({
                    "category": "qualification_enhancement",
                    "title": f"Address {gap['category'].capitalize()} Expectations",
                    "action": gap["description"],
                    "evidence": f"Identified gap with severity {gap['severity']}."
                })

        elapsed = (time.time() - start_time) * 1000
        return ToolResult(
            success=True,
            data={
                "recommendations": recommendations,
                "summary": {
                    "total_recommendations": len(recommendations)
                }
            },
            execution_time_ms=elapsed
        )
