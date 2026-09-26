# Resume & Job Matching Agent

[![Agent Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](agent.yaml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-independent-purple.svg)](SOUL.md)

An independent, portable, deterministic, and framework-independent AI agent for resume profiling, job description analysis, skill matching, qualification gap analysis, compatibility scoring, and application-readiness reporting.

---

## Overview

The **Resume & Job Matching Agent** (`resume-job-matching-agent-01`) analyzes candidate resumes against target job postings to deliver structured, evidence-grounded alignment reports. Built on a framework-independent architecture (`AgentCore`), it operates completely offline without mandatory external LLM API dependencies.

## Problem

Job seekers often struggle to identify how well their resume aligns with job descriptions, which keywords are missing, and where their qualifications fall short. Conversely, traditional automated tools are often opaque, hardcode rigid assumptions, or attempt to make discriminatory hiring predictions without transparent reasoning.

## Solution

This agent provides a transparent, deterministic matching solution that extracts technical skills, matches qualifications against job requirements, computes weighted compatibility scores with full mathematical breakdowns, pinpoints actionable gaps, and generates resume optimization recommendations—all grounded strictly in supplied input evidence while completely excluding non-job protected characteristics.

## Architecture

```
External Framework (LangChain / CrewAI / CLI)
        ↓
Framework Adapter / Portable Adapter
        ↓
     AgentCore (Single Source of Truth)
        ↓
  ExecutionEngine
        ↓
  PassportManager | ToolRegistry | BehaviorContract
        ↓
Modular Domain Tools (ResumeProfiler, JobProfiler, SkillMatcher, GapAnalyzer, CompatibilityAnalyzer, Recommender, ReportGenerator)
        ↓
Structured Compatibility Analysis Report
```

## Agent Lifecycle

Execution follows a strict 14-phase lifecycle defined in `contracts/behavior_contract.py`:

`INPUT` → `REQUEST_VALIDATION` → `PASSPORT_LOADING` → `CAPABILITY_VALIDATION` → `TOOL_DISCOVERY` → `RESUME_PROFILING` → `JOB_PROFILING` → `SKILL_MATCHING` → `GAP_ANALYSIS` → `COMPATIBILITY_ANALYSIS` → `RECOMMENDATION_GENERATION` → `REPORT_GENERATION` → `RESULT_VALIDATION` → `RESPONSE_GENERATION`

## Capabilities

1. `resume_profiling`: Extract verified skills, education, experience, and certifications.
2. `job_description_profiling`: Extract required skills, preferred skills, and experience expectations.
3. `skill_matching`: Compare candidate skills against job demands with explainable classification.
4. `qualification_gap_analysis`: Pinpoint missing skills and qualification gaps.
5. `compatibility_analysis`: Calculate deterministic score based on configurable criteria.
6. `recommendation_generation`: Generate practical, evidence-based recommendations.
7. `matching_report`: Assemble comprehensive structured analysis reports.

## Tools

- `tools/resume_profiler_tool.py`: Profile candidate resume.
- `tools/job_description_profiler_tool.py`: Profile job posting.
- `tools/skill_matching_tool.py`: Match skills and evidence.
- `tools/qualification_gap_tool.py`: Analyze missing requirements.
- `tools/compatibility_analyzer_tool.py`: Compute weighted compatibility score.
- `tools/recommendation_tool.py`: Formulate optimization suggestions.
- `tools/matching_report_tool.py`: Generate final JSON report.

## Input Format

Plain text strings or structured JSON objects:

```json
{
  "resume": "Software engineer with 4 years of experience in Python, SQL, Docker, and PostgreSQL. Bachelor's in CS.",
  "job_description": "Seeking Backend Engineer with Python, SQL, Docker, and Kubernetes experience. Bachelor's required."
}
```

## Output Format

A structured dictionary containing:
- `resume_profile`: Extracted skills, education, experience.
- `job_profile`: Extracted required & preferred skills.
- `skill_matching`: `matched_skills`, `partially_matched_skills`, `missing_skills`.
- `qualification_gaps`: Categorized gaps with severity levels.
- `compatibility_analysis`: Overall score, level (`HIGH`/`MODERATE`/`LOW`), score breakdown.
- `recommendations`: Actionable resume optimization advice.
- `limitations_and_disclaimer`: Ethical boundaries and non-hiring decision disclaimer.

## Matching Method

Offline deterministic tokenization, phrase matching, normalization, and configurable skill alias resolution (e.g. `JS` → `JavaScript`).

## Scoring Method

Calculated using configurable weights defined in `config/matching_config.json`:
- Required Skill Coverage: 40%
- Preferred Skill Coverage: 20%
- Experience Alignment: 20%
- Education Alignment: 10%
- Certification Alignment: 10%

## Explainability

All scores provide exact mathematical breakdowns. Matched skills reference candidate resume evidence, and missing skills detail target job requirements. See [EXPLAINABILITY.md](EXPLAINABILITY.md).

## Privacy

Candidate resumes are treated as sensitive data. The agent redacts phone numbers, emails, and SSNs in log streams and operates offline by default.

## Limitations

The agent is an analytical assistant and DOES NOT evaluate candidate hiring probability or replace human recruiters. Protected non-job characteristics are strictly excluded.

## Portability

Operates on standard Python primitives via `PortableAdapter` without external framework dependencies.

## Passport

Managed by `PassportManager` via `passport/passport.json` compliant with Agent Passport specification.

## Verification

Run verification scripts to dynamically audit passport integrity, security, hardcoding, portability, and local HiDevs readiness:
`python scripts/run_verification.py`

## Testing

Comprehensive test suite using `pytest`:
`pytest tests/ -v`

## Demo

Execute synthetic demonstration script:
`python scripts/demo.py`

## Installation

```bash
git clone <repository-url>
cd resume-job-matching-agent
pip install -r requirements.txt
```

## Usage

```python
from adapters.portable_adapter import PortableAdapter

adapter = PortableAdapter()
response = adapter.run(
    resume="Backend developer with Python, FastAPI, Docker, and PostgreSQL experience.",
    job_description="Looking for Python Developer proficient in FastAPI, Docker, and Redis."
)

print(response.result["compatibility_analysis"]["overall_compatibility_score"])
```

## Configuration

Weights, thresholds, and skill aliases can be updated in `config/matching_config.json`.

## Optional Provider Integration

Optional OpenAI model integration can be configured via `OPENAI_API_KEY` in `.env`.

## Security

Scanned automatically via `verification/security_audit.py` to prevent secret leaks and `.env` tracking.

## GitHub

Prepared for standalone repository deployment under `resume-job-matching-agent`.

## HiDevs Submission Readiness

Verified via local audit script `verification/hidevs_readiness.py`.
