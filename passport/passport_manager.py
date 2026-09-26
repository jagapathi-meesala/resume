"""PassportManager handles loading, validating, and retrieving Agent Passport metadata."""

import json
import os
from typing import Dict, Any, Optional, List
from contracts.passport_contract import PassportData, CapabilityDeclaration

PASSPORT_FILE_PATH = os.path.join(os.path.dirname(__file__), "passport.json")
SCHEMA_FILE_PATH = os.path.join(os.path.dirname(__file__), "passport_schema.json")


class PassportManager:
    """Manages the identity and capabilities defined in the agent passport."""

    def __init__(self, passport_path: str = PASSPORT_FILE_PATH, schema_path: str = SCHEMA_FILE_PATH):
        self.passport_path = passport_path
        self.schema_path = schema_path
        self._raw_data: Optional[Dict[str, Any]] = None
        self._passport_data: Optional[PassportData] = None

    def load_passport(self) -> PassportData:
        """Load and parse the passport JSON file."""
        if not os.path.exists(self.passport_path):
            raise FileNotFoundError(f"Passport file not found at {self.passport_path}")

        with open(self.passport_path, "r", encoding="utf-8") as f:
            self._raw_data = json.load(f)

        capabilities = [
            CapabilityDeclaration(
                name=cap["name"],
                description=cap["description"],
                tool=cap["tool"]
            )
            for cap in self._raw_data.get("capabilities", [])
        ]

        self._passport_data = PassportData(
            agent_id=self._raw_data.get("agent_id", ""),
            name=self._raw_data.get("name", ""),
            display_name=self._raw_data.get("display_name", ""),
            version=self._raw_data.get("version", ""),
            description=self._raw_data.get("description", ""),
            author=self._raw_data.get("author", ""),
            license=self._raw_data.get("license", ""),
            capabilities=capabilities,
            tools=self._raw_data.get("tools", []),
            lifecycle_phases=self._raw_data.get("lifecycle_phases", []),
            verification_status=self._raw_data.get("verification_status", {})
        )
        return self._passport_data

    def validate_schema(self) -> bool:
        """Validate passport data structure."""
        if self._raw_data is None:
            self.load_passport()

        required_keys = [
            "agent_id", "name", "display_name", "version",
            "capabilities", "tools", "lifecycle_phases", "portability"
        ]
        for key in required_keys:
            if key not in self._raw_data:
                raise ValueError(f"Passport schema validation failed: missing key '{key}'")
        return True

    def get_passport(self) -> PassportData:
        if self._passport_data is None:
            return self.load_passport()
        return self._passport_data

    def get_declared_capabilities(self) -> List[str]:
        passport = self.get_passport()
        return [cap.name for cap in passport.capabilities]

    def get_declared_tools(self) -> List[str]:
        passport = self.get_passport()
        return passport.tools
