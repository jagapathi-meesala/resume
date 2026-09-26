"""Script to run security audit, hardcoding audit, and HiDevs readiness check."""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from verification.security_audit import SecurityAudit
from verification.hardcoding_audit import HardcodingAudit
from verification.hidevs_readiness import HiDevsReadinessChecker


def main():
    print("============================================================")
    print("            RUNNING ALL CODEBASE AUDITS                     ")
    print("============================================================\n")

    sec = SecurityAudit().run_audit()
    print(f"[SECURITY AUDIT] Status: {sec['status']} | Findings: {sec['findings_count']}")
    if sec['findings']:
        print(f"  Findings: {sec['findings']}")

    hard = HardcodingAudit().run_audit()
    print(f"[HARDCODING AUDIT] Status: {hard['status']} | Violations: {hard['violations_count']}")
    if hard['violations']:
        print(f"  Violations: {hard['violations']}")

    hidevs = HiDevsReadinessChecker().check()
    print(f"[{hidevs['title']}] Status: {hidevs['status']} | Issues: {hidevs['issues_count']}")
    if hidevs['issues']:
        print(f"  Issues: {hidevs['issues']}")

    print("\nAudits finished.")


if __name__ == "__main__":
    main()
