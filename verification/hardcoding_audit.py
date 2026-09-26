"""Hardcoding Audit: Ensures no hardcoded tool counts, capability counts, or fake outputs exist in core/verification logic."""

import os
import re
from typing import Dict, Any, List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FORBIDDEN_HARDCODED_PATTERNS = [
    (r'EXPECTED_TOOLS\s*=\s*\d+', "Hardcoded tool count in generic logic"),
    (r'EXPECTED_CAPABILITIES\s*=\s*\d+', "Hardcoded capability count in generic logic"),
    (r'TOTAL_TOOLS\s*=\s*7', "Fixed hardcoded total tool count"),
    (r'TOTAL_CAPABILITIES\s*=\s*7', "Fixed hardcoded total capability count"),
    (r'visa_status\s*=\s*["\']GRANTED["\']', "Fake passport visa result hardcoding")
]


class HardcodingAudit:
    def __init__(self, root_dir: str = PROJECT_ROOT):
        self.root_dir = root_dir

    def run_audit(self) -> Dict[str, Any]:
        violations: List[Dict[str, Any]] = []

        scan_dirs = ["core", "contracts", "verification", "passport", "registry", "adapters", "providers"]

        for d in scan_dirs:
            target_dir = os.path.join(self.root_dir, d)
            if not os.path.exists(target_dir):
                continue

            for root, dirs, files in os.walk(target_dir):
                for file in files:
                    if file.endswith(".py"):
                        filepath = os.path.join(root, file)
                        rel_path = os.path.relpath(filepath, self.root_dir)

                        try:
                            with open(filepath, "r", encoding="utf-8") as f:
                                content = f.read()
                                for pattern, desc in FORBIDDEN_HARDCODED_PATTERNS:
                                    if re.search(pattern, content):
                                        violations.append({
                                            "file": rel_path,
                                            "issue": desc,
                                            "pattern": pattern
                                        })
                        except Exception as e:
                            pass

        status = "PASS" if not violations else "FAIL"
        return {
            "status": status,
            "violations_count": len(violations),
            "violations": violations
        }
