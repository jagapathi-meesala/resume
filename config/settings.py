"""Configuration loader and settings management for Resume & Job Matching Agent."""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Any, List

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "matching_config.json")


@dataclass
class MatchingSettings:
    weights: Dict[str, float] = field(default_factory=lambda: {
        "required_skills": 0.40,
        "preferred_skills": 0.20,
        "experience_alignment": 0.20,
        "education_alignment": 0.10,
        "certification_alignment": 0.10
    })
    skill_aliases: Dict[str, str] = field(default_factory=dict)
    skill_categories: Dict[str, List[str]] = field(default_factory=dict)
    score_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "high_match": 80.0,
        "moderate_match": 50.0
    })

    @classmethod
    def load_from_json(cls, file_path: str = CONFIG_FILE_PATH) -> "MatchingSettings":
        if not os.path.exists(file_path):
            return cls()
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            weights=data.get("weights", {}),
            skill_aliases={k.lower(): v.lower() for k, v in data.get("skill_aliases", {}).items()},
            skill_categories=data.get("skill_categories", {}),
            score_thresholds=data.get("score_thresholds", {})
        )

    def validate(self) -> bool:
        total_weight = sum(self.weights.values())
        if not (0.99 <= total_weight <= 1.01):
            raise ValueError(f"Matching weights must sum to 1.0, got {total_weight}")
        return True
