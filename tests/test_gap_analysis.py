"""Tests for QualificationGapTool."""

import pytest
from tools.qualification_gap_tool import QualificationGapTool


def test_qualification_gap_detection():
    tool = QualificationGapTool()
    input_data = {
        "skill_matching_result": {
            "missing_skills": [
                {"skill": "kubernetes", "requirement_type": "required"}
            ]
        },
        "resume_profile": {"skills": ["python"], "education": []},
        "job_profile": {"education_requirements": ["Bachelor's Degree"]}
    }
    res = tool.run(input_data)
    assert res.success is True
    gaps = res.data["gaps"]
    categories = [g["category"] for g in gaps]
    assert "required_skill" in categories
    assert "education" in categories
