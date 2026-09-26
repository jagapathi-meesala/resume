"""Tests for AgentCore lifecycle and processing."""

import pytest
from core.agent_core import AgentCore
from contracts.behavior_contract import LifecyclePhase


def test_agent_core_initialization():
    core = AgentCore()
    assert core.passport.agent_id == "resume-job-matching-agent-01"
    assert len(core.registry.list_tools()) >= 7


def test_agent_core_empty_request():
    core = AgentCore()
    res = core.process_request({})
    assert res.status == "FAILED"
    assert len(res.errors) > 0


def test_agent_core_successful_pipeline():
    core = AgentCore()
    payload = {
        "resume": "Software engineer proficient in Python, SQL, and Docker. Bachelor's in CS.",
        "job_description": "Backend engineer position requiring Python, SQL, and Docker."
    }
    res = core.process_request(payload)
    assert res.status == "SUCCESS"
    assert "matching_report" in res.result or "compatibility_analysis" in res.result
    assert res.execution_summary["total_phases_executed"] >= 14
