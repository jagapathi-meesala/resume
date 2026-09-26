# Explainability Specification

This document details the reasoning, data sources, scoring formulas, tool interactions, and verification mechanisms governing the **Resume & Job Matching Agent**.

## Purpose

The primary purpose of the agent is to deliver fully explainable, deterministic resume and job description matching reports without relying on opaque black-box machine learning models. By breaking down analysis into explicit skill extractions, evidence matching, and configurable scoring weights, users gain complete visibility into how compatibility evaluations are computed.

## Inputs and Data Sources

The agent accepts plain text strings or structured JSON objects representing a candidate resume and a target job description. All extractions, skill comparisons, and gap analyses operate strictly on the text provided within these input documents. No external or hardcoded real-world databases are queried, ensuring that evaluations remain completely grounded in user-supplied evidence.

## Decision and Reasoning

Matching reasoning combines exact phrase comparison, token normalization, and explicit alias mapping (e.g. mapping "JS" to "JavaScript"). The overall compatibility score is calculated using configurable weights: 40% for required skill coverage, 20% for preferred skill coverage, 20% for experience alignment, 10% for education, and 10% for certifications. Each numerical score is accompanied by an itemized mathematical breakdown detailing exactly how each sub-score contributed to the final total.

## Tools and Capabilities

The agent delegates tasks across seven modular domain tools: `resume_profiler_tool`, `job_description_profiler_tool`, `skill_matching_tool`, `qualification_gap_tool`, `compatibility_analyzer_tool`, `recommendation_tool`, and `matching_report_tool`. Each tool adheres to strict input/output contracts and registers dynamically with the central `ToolRegistry` to ensure transparent, inspectable execution.

## Limitations and Constraints

The agent operates strictly as an analytical assistant and does NOT make autonomous hiring decisions or predict hiring probability. Furthermore, the system strictly enforces non-discrimination by excluding all protected characteristics (such as race, gender, age, religion, or disability) from evaluation.

## Portability

The core execution engine (`AgentCore`) is framework-independent and requires no third-party orchestration framework or cloud LLM API to perform matching. Optional cloud providers are isolated behind a `ProviderBoundary` and framework adapters, ensuring that local offline execution is always preserved.

## Verification

The system includes a comprehensive dynamic verification suite comprising `PassportTrustVerifier`, `PortabilityVerifier`, `FrameworkVerifier`, `SecurityAudit`, `HardcodingAudit`, and `HiDevsReadinessChecker`. These verifiers dynamically inspect registered tools and passport metadata without relying on hardcoded assertions or static mock counts.

## Failure Handling

Invalid requests, missing fields, or empty document strings trigger structured error responses with clear diagnostic messages. All error text and exception logs are processed through a `PrivacyRedactor` to strip sensitive PII (such as emails, phone numbers, or SSNs) before returning responses.

## Expected Output

The final execution output is a structured dictionary containing extracted candidate profiles, extracted job requirements, matched skills with evidence, missing skills with justifications, qualification gaps, a weighted compatibility score with detailed breakdown, and actionable resume optimization recommendations. This output provides candidates and reviewers with an objective, evidence-based assessment ready for practical application.
