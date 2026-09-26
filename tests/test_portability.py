"""Tests for portability and framework verification."""

import pytest
from verification.portability_verifier import PortabilityVerifier
from verification.framework_verifier import FrameworkVerifier


def test_portability_verifier():
    verifier = PortabilityVerifier()
    res = verifier.verify()
    assert res["status"] == "PASS"


def test_framework_verifier():
    verifier = FrameworkVerifier()
    res = verifier.verify()
    assert res["status"] == "COMPLETED"
    assert res["details"]["adapter_structure_exists"] is True
