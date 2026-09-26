"""Synthetic Demonstration Script for Resume & Job Matching Agent."""

import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from adapters.portable_adapter import PortableAdapter

# Synthetic Candidate Profile (Demo Data)
SYNTHETIC_RESUME = """
ALEX RIVERS - Senior Software Engineer
Summary: Experienced Backend Engineer with 5+ years of experience building scalable microservices and database systems.

Skills:
- Programming: Python, SQL, JavaScript, Go
- Frameworks: FastAPI, Django, Flask
- Databases: PostgreSQL, Redis, MongoDB
- Cloud & Infrastructure: Docker, Git, Linux, AWS

Education:
- Bachelor of Science in Computer Science

Certifications:
- AWS Certified Solutions Architect
"""

# Synthetic Job Description (Demo Data)
SYNTHETIC_JOB_DESCRIPTION = """
Job Title: Senior Backend Developer (Python & Cloud)

Responsibilities:
- Design and maintain microservice APIs using Python and FastAPI.
- Manage high-performance PostgreSQL and Redis storage solutions.
- Deploy services using Docker and Kubernetes on AWS.

Requirements:
- 4+ years of professional software engineering experience.
- Strong proficiency in Python, PostgreSQL, Docker, and AWS.
- Bachelor's Degree in Computer Science or related field.

Preferred Qualifications:
- Experience with Kubernetes and Go.
- AWS Certification.
"""


def main():
    print("============================================================")
    print("      RESUME & JOB MATCHING AGENT - SYNTHETIC DEMO          ")
    print("============================================================\n")
    print("[NOTICE] All candidate profiles and job postings used herein are SYNTHETIC test data.\n")

    adapter = PortableAdapter()
    print("Executing deterministic offline matching pipeline...")
    response = adapter.run(
        resume=SYNTHETIC_RESUME,
        job_description=SYNTHETIC_JOB_DESCRIPTION
    )

    if response.status != "SUCCESS":
        print(f"[ERROR] Execution failed: {response.errors}")
        sys.exit(1)

    report = response.result
    compat = report["compatibility_analysis"]
    skills = report["skill_matching"]

    print("\n------------------------------------------------------------")
    print(" 1. CANDIDATE RESUME PROFILE (EXTRACTED)")
    print("------------------------------------------------------------")
    print(f"Extracted Skills: {report['resume_profile']['skills']}")
    print(f"Education: {report['resume_profile']['education']}")
    print(f"Certifications: {report['resume_profile']['certifications']}")

    print("\n------------------------------------------------------------")
    print(" 2. JOB POSTING REQUIREMENTS (EXTRACTED)")
    print("------------------------------------------------------------")
    print(f"Required Skills: {report['job_profile']['required_skills']}")
    print(f"Preferred Skills: {report['job_profile']['preferred_skills']}")

    print("\n------------------------------------------------------------")
    print(" 3. SKILL MATCHING CLASSIFICATION")
    print("------------------------------------------------------------")
    print("Matched Skills:")
    for m in skills["matched_skills"]:
        print(f"  [MATCHED] {m['skill']} ({m['requirement_type']}) -> Evidence: {m['resume_evidence']}")

    print("\nMissing Skills:")
    for m in skills["missing_skills"]:
        print(f"  [MISSING] {m['skill']} ({m['requirement_type']}) -> Reason: {m['reason']}")

    print("\n------------------------------------------------------------")
    print(" 4. COMPATIBILITY SCORING & EXPLANATION")
    print("------------------------------------------------------------")
    print(f"Overall Score      : {compat['overall_compatibility_score']}% ({compat['compatibility_level']})")
    print(f"Explanation        : {compat['explanation']}")
    print(f"Score Breakdown    : {compat['score_breakdown']}")

    print("\n------------------------------------------------------------")
    print(" 5. ACTIONABLE RECOMMENDATIONS")
    print("------------------------------------------------------------")
    for rec in report["recommendations"]:
        print(f"  - [{rec['category'].upper()}] {rec['title']}: {rec['action']}")

    print("\n------------------------------------------------------------")
    print(" 6. DISCLAIMER & LIMITATIONS")
    print("------------------------------------------------------------")
    for d in report["limitations_and_disclaimer"]:
        print(f"  - {d}")

    print("\n[SUCCESS] Demo completed successfully.\n")


if __name__ == "__main__":
    main()
