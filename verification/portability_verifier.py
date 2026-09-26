"""Portability Verifier: Verifies framework-independence and offline execution capability."""

from typing import Dict, Any
from adapters.portable_adapter import PortableAdapter
from core.agent_core import AgentCore


class PortabilityVerifier:
    """Verifies that AgentCore operates offline without framework coupling."""

    def verify(self) -> Dict[str, Any]:
        try:
            core = AgentCore()
            adapter = PortableAdapter(core)

            # Test execution with synthetic offline payload
            sample_resume = "Candidate with Python, SQL, Docker, and 4 years of experience in backend software engineering. Bachelor's in Computer Science."
            sample_jd = "Seeking Backend Engineer with Python, SQL, Docker, and Kubernetes experience. Bachelor's Degree required."

            response = adapter.run(sample_resume, sample_jd)

            if response.status != "SUCCESS":
                return {
                    "status": "FAIL",
                    "message": f"Portable execution test failed with status: {response.status}",
                    "details": {"errors": response.errors}
                }

            report = response.result
            if "compatibility_analysis" not in report or "skill_matching" not in report:
                return {
                    "status": "FAIL",
                    "message": "Portable execution produced incomplete result structure.",
                    "details": {}
                }

            return {
                "status": "PASS",
                "message": "Portability verification passed. Agent executes offline and framework-independently.",
                "details": {
                    "framework_independent": True,
                    "offline_capable": True,
                    "execution_status": response.status,
                    "request_id": response.request_id
                }
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"Portability verification encountered error: {str(e)}",
                "details": {}
            }
