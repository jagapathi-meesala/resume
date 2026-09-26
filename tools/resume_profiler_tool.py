"""Resume Profiler Tool: Analyzes plain text or structured resume to extract skills, education, and experience."""

import re
import time
from typing import Dict, Any, List, Set
from contracts.tool_contract import BaseTool, ToolResult
from config.settings import MatchingSettings


class ResumeProfilerTool(BaseTool):
    def __init__(self, settings: MatchingSettings = None):
        super().__init__(
            name="resume_profiler_tool",
            description="Analyzes plain text or structured JSON resume to extract verified skills, education, experience, and certifications.",
            capability="resume_profiling"
        )
        self.settings = settings or MatchingSettings.load_from_json()

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        return "resume" in input_data and input_data["resume"] is not None

    def run(self, input_data: Dict[str, Any]) -> ToolResult:
        start_time = time.time()
        resume_raw = input_data.get("resume")

        if isinstance(resume_raw, dict):
            profile = self._parse_structured_resume(resume_raw)
        elif isinstance(resume_raw, str):
            profile = self._parse_text_resume(resume_raw)
        else:
            return ToolResult(
                success=False,
                data={},
                error="Unsupported resume format. Expected plain text string or structured dict."
            )

        elapsed = (time.time() - start_time) * 1000
        return ToolResult(
            success=True,
            data={"resume_profile": profile},
            execution_time_ms=elapsed
        )

    def _parse_structured_resume(self, data: Dict[str, Any]) -> Dict[str, Any]:
        extracted_skills = data.get("skills", [])
        if isinstance(extracted_skills, str):
            extracted_skills = [s.strip() for s in extracted_skills.split(",")]

        # Normalize skills
        normalized_skills = []
        for s in extracted_skills:
            if isinstance(s, str) and s.strip():
                normalized_skills.append(s.strip())

        return {
            "skills": sorted(list(set(normalized_skills))),
            "technologies": data.get("technologies", []),
            "programming_languages": data.get("programming_languages", []),
            "tools": data.get("tools", []),
            "education": data.get("education", []),
            "certifications": data.get("certifications", []),
            "projects": data.get("projects", []),
            "experience": data.get("experience", []),
            "responsibilities": data.get("responsibilities", []),
            "achievements": data.get("achievements", []),
            "raw_text_length": len(str(data))
        }

    def _parse_text_resume(self, text: str) -> Dict[str, Any]:
        lowered_text = text.lower()

        # Known vocabulary lookup based on settings categories & aliases
        found_skills: Set[str] = set()
        all_vocab = set()
        for cat, skills_list in self.settings.skill_categories.items():
            all_vocab.update(skills_list)
        all_vocab.update(self.settings.skill_aliases.keys())
        all_vocab.update(self.settings.skill_aliases.values())

        for vocab in all_vocab:
            # Word boundary regex search
            pattern = r'\b' + re.escape(vocab) + r'\b'
            if re.search(pattern, lowered_text):
                # Standardize alias if present
                canonical = self.settings.skill_aliases.get(vocab, vocab)
                found_skills.add(canonical)

        # Extract explicit skill lines (e.g. "Skills: Python, Docker, React")
        skill_section_match = re.search(r'(?:skills|technical skills|technologies)\s*:\s*([^\n]+)', text, re.IGNORECASE)
        if skill_section_match:
            raw_skills = skill_section_match.group(1).split(',')
            for s in raw_skills:
                cleaned = s.strip().strip('.').lower()
                if cleaned:
                    canonical = self.settings.skill_aliases.get(cleaned, cleaned)
                    found_skills.add(canonical)

        # Extract Education keywords
        education = []
        edu_patterns = [r'\b(bachelor|master|phd|b\.s\.|m\.s\.|b\.a\.|m\.a\.|degree|diploma)\b']
        for p in edu_patterns:
            matches = re.findall(p, text, re.IGNORECASE)
            for m in matches:
                education.append(m.capitalize())

        # Extract Certifications
        certifications = []
        cert_patterns = [r'\b(certified|certification|aws certified|pmp|cissp|scrum master|ckad|cka)\b']
        for p in cert_patterns:
            matches = re.findall(p, text, re.IGNORECASE)
            for m in matches:
                certifications.append(m.upper())

        # Extract experience mentions (e.g. "5 years of experience")
        experience = []
        exp_matches = re.findall(r'(\d+\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)?)', text, re.IGNORECASE)
        for m in exp_matches:
            experience.append(m.strip())

        return {
            "skills": sorted(list(found_skills)),
            "technologies": sorted([s for s in found_skills if s in self.settings.skill_categories.get("tools_and_platforms", []) or s in self.settings.skill_categories.get("frameworks", [])]),
            "programming_languages": sorted([s for s in found_skills if s in self.settings.skill_categories.get("programming_languages", [])]),
            "tools": sorted([s for s in found_skills if s in self.settings.skill_categories.get("tools_and_platforms", [])]),
            "education": list(set(education)),
            "certifications": list(set(certifications)),
            "projects": [],
            "experience": list(set(experience)),
            "responsibilities": [],
            "achievements": [],
            "raw_text_length": len(text)
        }
