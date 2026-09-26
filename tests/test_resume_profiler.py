"""Tests for ResumeProfilerTool."""

import pytest
from tools.resume_profiler_tool import ResumeProfilerTool


def test_resume_profiler_text():
    tool = ResumeProfilerTool()
    text = "Candidate with Python, JavaScript, PostgreSQL experience. Degree: Bachelor of Science."
    result = tool.run({"resume": text})

    assert result.success is True
    profile = result.data["resume_profile"]
    assert "python" in profile["skills"]
    assert "javascript" in profile["skills"]
    assert "postgresql" in profile["skills"]
    assert len(profile["education"]) > 0


def test_resume_profiler_structured():
    tool = ResumeProfilerTool()
    data = {
        "skills": ["Python", "Docker"],
        "education": ["B.S. Computer Science"]
    }
    result = tool.run({"resume": data})
    assert result.success is True
    profile = result.data["resume_profile"]
    assert "Python" in profile["skills"]
