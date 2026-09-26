"""Compatibility Analyzer Tool: Computes deterministic compatibility scores with full mathematical breakdown."""

import time
from typing import Dict, Any
from contracts.tool_contract import BaseTool, ToolResult
from config.settings import MatchingSettings


class CompatibilityAnalyzerTool(BaseTool):
    def __init__(self, settings: MatchingSettings = None):
        super().__init__(
            name="compatibility_analyzer_tool",
            description="Calculates a deterministic, explainable compatibility score based on configurable weights and empirical evidence.",
            capability="compatibility_analysis"
        )
        self.settings = settings or MatchingSettings.load_from_json()

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        return "skill_matching_result" in input_data and "gap_analysis_result" in input_data

    def run(self, input_data: Dict[str, Any]) -> ToolResult:
        start_time = time.time()
        skill_match = input_data["skill_matching_result"]
        gap_analysis = input_data["gap_analysis_result"]
        weights = self.settings.weights

        matched_skills = skill_match.get("matched_skills", [])
        partial_skills = skill_match.get("partially_matched_skills", [])
        missing_skills = skill_match.get("missing_skills", [])

        # Required skill score
        req_matched = sum(1 for m in matched_skills if m.get("requirement_type") == "required")
        req_partial = sum(1 for m in partial_skills if m.get("requirement_type") == "required")
        req_missing = sum(1 for m in missing_skills if m.get("requirement_type") == "required")
        total_req = req_matched + req_partial + req_missing

        req_score = 100.0 if total_req == 0 else ((req_matched + (0.5 * req_partial)) / total_req) * 100.0

        # Preferred skill score
        pref_matched = sum(1 for m in matched_skills if m.get("requirement_type") == "preferred")
        pref_missing = sum(1 for m in missing_skills if m.get("requirement_type") == "preferred")
        total_pref = pref_matched + pref_missing

        pref_score = 100.0 if total_pref == 0 else (pref_matched / total_pref) * 100.0

        # Education & Experience alignment scores
        gaps = gap_analysis.get("gaps", [])
        has_edu_gap = any(g["category"] == "education" for g in gaps)
        has_exp_gap = any(g["category"] == "experience" for g in gaps)

        edu_score = 50.0 if has_edu_gap else 100.0
        exp_score = 60.0 if has_exp_gap else 100.0
        cert_score = 100.0  # Baseline unless cert gaps present

        # Weighted final score
        final_score = (
            (req_score * weights.get("required_skills", 0.40)) +
            (pref_score * weights.get("preferred_skills", 0.20)) +
            (exp_score * weights.get("experience_alignment", 0.20)) +
            (edu_score * weights.get("education_alignment", 0.10)) +
            (cert_score * weights.get("certification_alignment", 0.10))
        )
        final_score = round(min(100.0, max(0.0, final_score)), 2)

        # Classification label
        if final_score >= self.settings.score_thresholds.get("high_match", 80.0):
            compatibility_level = "HIGH"
        elif final_score >= self.settings.score_thresholds.get("moderate_match", 50.0):
            compatibility_level = "MODERATE"
        else:
            compatibility_level = "LOW"

        breakdown = {
            "required_skills_score": round(req_score, 2),
            "preferred_skills_score": round(pref_score, 2),
            "experience_alignment_score": round(exp_score, 2),
            "education_alignment_score": round(edu_score, 2),
            "certification_alignment_score": round(cert_score, 2),
            "applied_weights": weights
        }

        explanation = (
            f"Compatibility score of {final_score}% ({compatibility_level}) calculated deterministically. "
            f"Required skill match rate is {round(req_score, 1)}% (weight {weights.get('required_skills')}), "
            f"preferred skill match rate is {round(pref_score, 1)}% (weight {weights.get('preferred_skills')}). "
            f"Note: This score evaluates document keyword/skill alignment and DOES NOT predict hiring outcomes or candidate job performance."
        )

        elapsed = (time.time() - start_time) * 1000
        return ToolResult(
            success=True,
            data={
                "overall_compatibility_score": final_score,
                "compatibility_level": compatibility_level,
                "score_breakdown": breakdown,
                "explanation": explanation,
                "disclaimer": "This analytical compatibility score reflects input alignment only and does NOT constitute a hiring decision."
            },
            execution_time_ms=elapsed
        )
