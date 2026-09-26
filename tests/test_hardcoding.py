"""Tests for HardcodingAudit."""

import pytest
from verification.hardcoding_audit import HardcodingAudit


def test_hardcoding_audit():
    audit = HardcodingAudit()
    res = audit.run_audit()
    assert res["status"] == "PASS"
    assert res["violations_count"] == 0
