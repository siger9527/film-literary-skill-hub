import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[1]

class ResourceSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "schemas" / "resource-card.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def valid_card(self):
        return {
            "repository": "example/skill",
            "commit": "0123456789abcdef0123456789abcdef01234567",
            "path": "skills/example/SKILL.md",
            "skill_name": "Example Skill",
            "source_url": "https://github.com/example/skill/blob/0123456789abcdef0123456789abcdef01234567/skills/example/SKILL.md",
            "license_status": "LICENSED_REVIEW_REQUIRED",
            "license_file": "LICENSE",
            "license_spdx": "MIT",
            "license_evidence_url": "https://github.com/example/skill/blob/0123456789abcdef0123456789abcdef01234567/LICENSE",
            "review_status": "DISCOVERED",
            "source_text_read": True,
            "categories": ["screenwriting"],
            "evidence": ["commit-pinned source"],
            "discovered_at": "2026-11-01T00:00:00+00:00"
        }

    def test_valid_card(self):
        self.assertTrue(self.validator.is_valid(self.valid_card()))

    def test_missing_source_read_flag_is_rejected(self):
        card = self.valid_card()
        del card["source_text_read"]
        self.assertFalse(self.validator.is_valid(card))

    def test_unknown_field_is_rejected(self):
        card = self.valid_card()
        card["unreviewed_field"] = "unexpected"
        self.assertFalse(self.validator.is_valid(card))

    def test_invalid_commit_is_rejected(self):
        card = self.valid_card()
        card["commit"] = "not-a-sha"
        self.assertFalse(self.validator.is_valid(card))

if __name__ == "__main__":
    unittest.main()
