"""Security Audit: Scans codebase for secret leaks, API keys, and unsafe logging."""

import os
import re
from typing import Dict, Any, List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SECRET_PATTERNS = [
    (r'sk-[a-zA-Z0-9]{32,}', "Hardcoded OpenAI API Key"),
    (r'AKIA[0-9A-Z]{16}', "Hardcoded AWS Access Key"),
    (r'ghp_[a-zA-Z0-9]{36}', "Hardcoded GitHub Personal Access Token"),
    (r'-----BEGIN' + r' PRIVATE KEY-----', "Hardcoded Private Key"),
    (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded Password")
]


class SecurityAudit:
    def __init__(self, root_dir: str = PROJECT_ROOT):
        self.root_dir = root_dir

    def run_audit(self) -> Dict[str, Any]:
        findings: List[Dict[str, Any]] = []

        # Check .env tracking
        gitignore_path = os.path.join(self.root_dir, ".gitignore")
        env_ignored = False
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r", encoding="utf-8") as f:
                content = f.read()
                if ".env" in content:
                    env_ignored = True

        if not env_ignored:
            findings.append({
                "severity": "HIGH",
                "file": ".gitignore",
                "issue": ".env file is not explicitly listed in .gitignore"
            })

        # Scan python and configuration files
        for root, dirs, files in os.walk(self.root_dir):
            if ".git" in dirs:
                dirs.remove(".git")
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")
            if ".pytest_cache" in dirs:
                dirs.remove(".pytest_cache")

            for file in files:
                if file.endswith((".py", ".json", ".yaml", ".yml", ".md")):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, self.root_dir)
                    if file == ".env.example":
                        continue

                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            text = f.read()
                            for pattern, desc in SECRET_PATTERNS:
                                if re.search(pattern, text):
                                    findings.append({
                                        "severity": "CRITICAL",
                                        "file": rel_path,
                                        "issue": desc
                                    })
                    except Exception as e:
                        pass

        status = "PASS" if not findings else "FAIL"
        return {
            "status": status,
            "findings_count": len(findings),
            "findings": findings,
            "env_protected": env_ignored
        }
