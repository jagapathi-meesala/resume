"""Tests for JobDescriptionProfilerTool."""

import pytest
from tools.job_description_profiler_tool import JobDescriptionProfilerTool


def test_job_profiler_text():
    tool = JobDescriptionProfilerTool()
    text = "We require Python, SQL, and Docker. Preferred: Kubernetes."
    result = tool.run({"job_description": text})

    assert result.success is True
    profile = result.data["job_profile"]
    assert "python" in profile["required_skills"]
    assert "sql" in profile["required_skills"]
    assert "docker" in profile["required_skills"]
    assert "kubernetes" in profile["preferred_skills"]
