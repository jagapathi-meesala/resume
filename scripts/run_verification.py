"""Final Verification Orchestrator Script for Resume & Job Matching Agent."""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from verification.passport_trust_verifier import PassportTrustVerifier
from verification.portability_verifier import PortabilityVerifier
from verification.framework_verifier import FrameworkVerifier
from verification.security_audit import SecurityAudit
from verification.hardcoding_audit import HardcodingAudit
from verification.hidevs_readiness import HiDevsReadinessChecker
from core.agent_core import AgentCore
from contracts.behavior_contract import BehaviorContract


def main():
    print("============================================================")
    print("      RESUME & JOB MATCHING AGENT - SYSTEM VERIFICATION     ")
    print("============================================================\n")

    results = {}

    # 1. Passport Trust Verification
    p_verifier = PassportTrustVerifier()
    results["passport_trust_verification"] = p_verifier.verify()

    # 2. ToolRegistry & AgentCore Validation
    try:
        core = AgentCore()
        tools_discovered = core.registry.list_tools()
        caps_discovered = core.registry.list_capabilities()
        results["tool_registry_validation"] = {
            "status": "PASS",
            "tools_count": len(tools_discovered),
            "capabilities_count": len(caps_discovered),
            "tools": tools_discovered,
            "capabilities": caps_discovered
        }
    except Exception as e:
        results["tool_registry_validation"] = {
            "status": "FAIL",
            "error": str(e)
        }

    # 3. Behavior Contract Validation
    try:
        seq = BehaviorContract.get_lifecycle_sequence()
        results["behavior_contract_validation"] = {
            "status": "PASS",
            "lifecycle_phases_count": len(seq)
        }
    except Exception as e:
        results["behavior_contract_validation"] = {
            "status": "FAIL",
            "error": str(e)
        }

    # 4. Portability Verification
    port_verifier = PortabilityVerifier()
    results["portability_verification"] = port_verifier.verify()

    # 5. Framework Verification
    fw_verifier = FrameworkVerifier()
    results["framework_verification"] = fw_verifier.verify()

    # 6. Security Audit
    sec_audit = SecurityAudit()
    results["security_audit"] = sec_audit.run_audit()

    # 7. Hardcoding Audit
    hard_audit = HardcodingAudit()
    results["hardcoding_audit"] = hard_audit.run_audit()

    # 8. HiDevs Readiness Audit
    hidevs_checker = HiDevsReadinessChecker()
    results["hidevs_readiness"] = hidevs_checker.check()

    # Print Summary Table
    print(f"{'CHECK':<35} | {'STATUS':<15}")
    print("-" * 55)
    for check_name, res in results.items():
        status = res.get("status", "UNKNOWN")
        print(f"{check_name:<35} | {status:<15}")

    print("\n------------------------------------------------------------")
    print("DETAILED VERIFICATION RESULTS (JSON):")
    print("------------------------------------------------------------")
    print(json.dumps(results, indent=2))

    # Overall Status check
    all_pass = all(
        res.get("status") in ("PASS", "COMPLETED")
        for res in results.values()
    )

    if all_pass:
        print("\n[VERIFICATION RESULT] OVERALL VERIFICATION: PASS")
    else:
        print("\n[VERIFICATION RESULT] OVERALL VERIFICATION: ISSUES DETECTED")

    return results


if __name__ == "__main__":
    main()
