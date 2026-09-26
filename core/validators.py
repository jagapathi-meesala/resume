"""Validators module for request schema validation and sensitive PII redactor."""

import re
from typing import Dict, Any, Tuple


class RequestValidator:
    """Validates raw incoming agent requests."""

    @staticmethod
    def validate_request(request_data: Dict[str, Any]) -> Tuple[bool, str]:
        if not isinstance(request_data, dict):
            return False, "Request payload must be a JSON object / dictionary."

        if "resume" not in request_data or request_data["resume"] is None:
            return False, "Missing mandatory field 'resume' in request payload."

        if "job_description" not in request_data or request_data["job_description"] is None:
            return False, "Missing mandatory field 'job_description' in request payload."

        resume = request_data["resume"]
        if isinstance(resume, str) and not resume.strip():
            return False, "'resume' text cannot be empty."

        jd = request_data["job_description"]
        if isinstance(jd, str) and not jd.strip():
            return False, "'job_description' text cannot be empty."

        return True, "Valid request"


class PrivacyRedactor:
    """Redacts common sensitive PII (emails, phone numbers, SSNs) from logs/messages."""

    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    PHONE_PATTERN = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        if not isinstance(text, str):
            return text
        sanitized = re.sub(cls.EMAIL_PATTERN, "[REDACTED_EMAIL]", text)
        sanitized = re.sub(cls.PHONE_PATTERN, "[REDACTED_PHONE]", sanitized)
        sanitized = re.sub(cls.SSN_PATTERN, "[REDACTED_SSN]", sanitized)
        return sanitized
