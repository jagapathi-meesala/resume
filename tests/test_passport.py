"""Tests for PassportManager and PassportTrustVerifier."""

import pytest
from passport.passport_manager import PassportManager
from verification.passport_trust_verifier import PassportTrustVerifier


def test_passport_manager_load():
    pm = PassportManager()
    data = pm.get_passport()
    assert data.agent_id == "resume-job-matching-agent-01"
    assert len(data.capabilities) >= 7
    assert len(data.tools) >= 7


def test_passport_trust_verifier():
    verifier = PassportTrustVerifier()
    res = verifier.verify()
    assert res["status"] == "PASS"
