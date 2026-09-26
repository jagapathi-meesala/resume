"""Job Description Profiler Tool: Analyzes plain text or structured job posting to extract requirements."""

import re
import time
from typing import Dict, Any, List, Set
from contracts.tool_contract import BaseTool, ToolResult
from config.settings import MatchingSettings


class JobDescriptionProfilerTool(BaseTool):
    def __init__(self, settings: MatchingSettings = None):
        super().__init__(
            name="job_description_profiler_tool",
            description="Analyzes plain text or structured job descriptions to extract required skills, preferred skills, experience, and education expectations.",
            capability="job_description_profiling"
        )
        self.settings = settings or MatchingSettings.load_from_json()

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if not isinstance(input_data, dict):
            return False
        return "job_description" in input_data and input_data["job_description"] is not None

    def run(self, input_data: Dict[str, Any]) -> ToolResult:
        start_time = time.time()
        jd_raw = input_data.get("job_description")

        if isinstance(jd_raw, dict):
            profile = self._parse_structured_jd(jd_raw)
        elif isinstance(jd_raw, str):
            profile = self._parse_text_jd(jd_raw)
        else:
            return ToolResult(
                success=False,
                data={},
                error="Unsupported job description format. Expected plain text string or structured dict."
            )

        elapsed = (time.time() - start_time) * 1000
        return ToolResult(
            success=True,
            data={"job_profile": profile},
            execution_time_ms=elapsed
        )

    def _parse_structured_jd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        req_skills = [self.settings.skill_aliases.get(s.lower(), s.lower()) for s in data.get("required_skills", [])]
        pref_skills = [self.settings.skill_aliases.get(s.lower(), s.lower()) for s in data.get("preferred_skills", [])]

        return {
            "required_skills": sorted(list(set(req_skills))),
            "preferred_skills": sorted(list(set(pref_skills))),
            "technologies": data.get("technologies", []),
            "responsibilities": data.get("responsibilities", []),
            "qualifications": data.get("qualifications", []),
            "experience_requirements": data.get("experience_requirements", []),
            "education_requirements": data.get("education_requirements", []),
            "job_relevant_keywords": sorted(list(set(req_skills + pref_skills)))
        }

    def _parse_text_jd(self, text: str) -> Dict[str, Any]:
        lowered = text.lower()

        found_required: Set[str] = set()
        found_preferred: Set[str] = set()

        all_vocab = set()
        for cat, skills_list in self.settings.skill_categories.items():
            all_vocab.update(skills_list)
        all_vocab.update(self.settings.skill_aliases.keys())
        all_vocab.update(self.settings.skill_aliases.values())

        # Distinguish sections (Required vs Preferred / Nice to have)
        pref_section_match = re.search(r'(?:preferred|nice to have|plus|bonus)\s*:\s*([^\n]+)', text, re.IGNORECASE)
        pref_skills_in_section = set()
        if pref_section_match:
            raw_pref = pref_section_match.group(1).split(',')
            for s in raw_pref:
                cleaned = s.strip().strip('.').lower()
                if cleaned:
                    canonical = self.settings.skill_aliases.get(cleaned, cleaned)
                    pref_skills_in_section.add(canonical)

        for vocab in all_vocab:
            pattern = r'\b' + re.escape(vocab) + r'\b'
            if re.search(pattern, lowered):
                canonical = self.settings.skill_aliases.get(vocab, vocab)
                if canonical in pref_skills_in_section:
                    found_preferred.add(canonical)
                else:
                    found_required.add(canonical)

        # Experience requirements pattern
        exp_reqs = re.findall(r'(\d+\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)?[^\.\n]*)', text, re.IGNORECASE)

        # Education requirements
        edu_reqs = []
        if re.search(r'\b(bachelor|b\.s\.|b\.a\.)\b', text, re.IGNORECASE):
            edu_reqs.append("Bachelor's Degree")
        if re.search(r'\b(master|m\.s\.|m\.a\.)\b', text, re.IGNORECASE):
            edu_reqs.append("Master's Degree")
        if re.search(r'\b(phd|doctorate)\b', text, re.IGNORECASE):
            edu_reqs.append("PhD")

        return {
            "required_skills": sorted(list(found_required)),
            "preferred_skills": sorted(list(found_preferred)),
            "technologies": sorted(list(found_required.union(found_preferred))),
            "responsibilities": [],
            "qualifications": [],
            "experience_requirements": [e.strip() for e in exp_reqs],
            "education_requirements": edu_reqs,
            "job_relevant_keywords": sorted(list(found_required.union(found_preferred)))
        }
