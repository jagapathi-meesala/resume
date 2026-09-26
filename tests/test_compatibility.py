"""Tests for CompatibilityAnalyzerTool."""

import pytest
from tools.compatibility_analyzer_tool import CompatibilityAnalyzerTool


def test_compatibility_scoring():
    tool = CompatibilityAnalyzerTool()
    input_data = {
        "skill_matching_result": {
            "matched_skills": [{"requirement_type": "required"}],
            "partially_matched_skills": [],
            "missing_skills": []
        },
        "gap_analysis_result": {"gaps": []}
    }
    res = tool.run(input_data)
    assert res.success is True
    assert res.data["overall_compatibility_score"] == 100.0
    assert res.data["compatibility_level"] == "HIGH"
    assert "explanation" in res.data
