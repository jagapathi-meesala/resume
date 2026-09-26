"""Tests for RecommendationTool."""

import pytest
from tools.recommendation_tool import RecommendationTool


def test_recommendation_generation():
    tool = RecommendationTool()
    input_data = {
        "skill_matching_result": {
            "matched_skills": [{"skill": "python", "requirement_type": "required"}],
            "partially_matched_skills": [],
            "missing_skills": [{"skill": "docker", "requirement_type": "required"}]
        },
        "gap_analysis_result": {"gaps": []}
    }
    res = tool.run(input_data)
    assert res.success is True
    recs = res.data["recommendations"]
    assert len(recs) >= 2
