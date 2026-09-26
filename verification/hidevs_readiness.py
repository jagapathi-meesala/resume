"""HiDevs Readiness Checker: Performs Local HiDevs Readiness Audit on root documentation and specifications."""

import os
import yaml
from typing import Dict, Any, List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

REQUIRED_EXPLAINABILITY_HEADINGS = [
    "Purpose",
    "Inputs and Data Sources",
    "Decision and Reasoning",
    "Tools and Capabilities",
    "Limitations and Constraints",
    "Portability",
    "Verification",
    "Failure Handling",
    "Expected Output"
]


class HiDevsReadinessChecker:
    def __init__(self, root_dir: str = PROJECT_ROOT):
        self.root_dir = root_dir

    def check(self) -> Dict[str, Any]:
        """Perform Local HiDevs Readiness Audit."""
        issues: List[str] = []

        # 1. agent.yaml check
        agent_yaml_path = os.path.join(self.root_dir, "agent.yaml")
        if not os.path.exists(agent_yaml_path):
            issues.append("Missing root file 'agent.yaml'")
        else:
            try:
                with open(agent_yaml_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data.get("spec_version") != "0.1.0":
                        issues.append(f"agent.yaml spec_version must be '0.1.0', got '{data.get('spec_version')}'")
                    name = data.get("name", "")
                    if name != "resume-job-matching-agent":
                        issues.append(f"agent.yaml name must be 'resume-job-matching-agent', got '{name}'")
                    allowed_keys = {"spec_version", "name", "version", "description", "author", "license", "tools", "model", "extends", "dependencies", "skills", "agents", "delegation", "runtime", "a2a", "compliance", "tags", "metadata"}
                    extra_keys = set(data.keys()) - allowed_keys
                    if extra_keys:
                        issues.append(f"agent.yaml contains unauthorized additional properties: {extra_keys}")
            except Exception as e:
                issues.append(f"Error parsing agent.yaml: {str(e)}")

        # 2. SOUL.md check
        soul_path = os.path.join(self.root_dir, "SOUL.md")
        if not os.path.exists(soul_path):
            issues.append("Missing root file 'SOUL.md'")
        else:
            with open(soul_path, "r", encoding="utf-8") as f:
                content = f.read()
                if len(content.strip()) < 100:
                    issues.append("SOUL.md content is too brief / empty boilerplate.")

        # 3. DUTIES.md check
        duties_path = os.path.join(self.root_dir, "DUTIES.md")
        if not os.path.exists(duties_path):
            issues.append("Missing root file 'DUTIES.md'")

        # 4. EXPLAINABILITY.md check
        explain_path = os.path.join(self.root_dir, "EXPLAINABILITY.md")
        if not os.path.exists(explain_path):
            issues.append("Missing root file 'EXPLAINABILITY.md'")
        else:
            with open(explain_path, "r", encoding="utf-8") as f:
                content = f.read()
                for heading in REQUIRED_EXPLAINABILITY_HEADINGS:
                    if f"## {heading}" not in content:
                        issues.append(f"EXPLAINABILITY.md missing required heading: '## {heading}'")

        status = "PASS" if not issues else "FAIL"
        return {
            "title": "LOCAL HIDEVS READINESS CHECK",
            "status": status,
            "issues_count": len(issues),
            "issues": issues
        }
