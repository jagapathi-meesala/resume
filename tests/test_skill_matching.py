"""Tests for SkillMatchingTool."""

import pytest
from tools.skill_matching_tool import SkillMatchingTool


def test_skill_matching_exact_and_missing():
    tool = SkillMatchingTool()
    input_data = {
        "resume_profile": {"skills": ["python", "docker"]},
        "job_profile": {
            "required_skills": ["python", "kubernetes"],
            "preferred_skills": ["docker"]
        }
    }
    res = tool.run(input_data)
    assert res.success is True
    matched = [m["skill"] for m in res.data["matched_skills"]]
    missing = [m["skill"] for m in res.data["missing_skills"]]

    assert "python" in matched
    assert "docker" in matched
    assert "kubernetes" in missing
