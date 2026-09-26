"""Tests for MatchingReportTool."""

import pytest
from tools.matching_report_tool import MatchingReportTool


def test_matching_report_assembly():
    tool = MatchingReportTool()
    input_data = {
        "resume_profile": {"skills": ["python"], "raw_text_length": 50},
        "job_profile": {"job_relevant_keywords": ["python"]},
        "skill_matching_result": {"matched_skills": [], "summary": {}},
        "gap_analysis_result": {"gaps": []},
        "compatibility_result": {"overall_compatibility_score": 90.0},
        "recommendations_result": {"recommendations": []}
    }
    res = tool.run(input_data)
    assert res.success is True
    report = res.data["matching_report"]
    assert report["report_header"]["agent_name"] == "resume-job-matching-agent"
    assert "limitations_and_disclaimer" in report
