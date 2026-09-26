"""Tests for SecurityAudit."""

import pytest
from verification.security_audit import SecurityAudit


def test_security_audit():
    audit = SecurityAudit()
    res = audit.run_audit()
    assert res["status"] == "PASS"
    assert res["env_protected"] is True
    assert res["findings_count"] == 0
