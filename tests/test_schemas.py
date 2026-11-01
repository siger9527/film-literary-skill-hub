import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator
import yaml

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

    def test_workflow_and_issue_form_yaml_parse(self):
        for path in [ROOT / ".github" / "workflows" / "discover.yml",
                     ROOT / ".github" / "workflows" / "quality-gate.yml",
                     ROOT / ".github" / "ISSUE_TEMPLATE" / "project-control.yml"]:
            with self.subTest(path=str(path)):
                parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertIsInstance(parsed, dict)

    def test_l2_review_schema_accepts_and_rejects_records(self):
        schema = json.loads((ROOT / "schemas" / "l2-review.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        record = {
            "repository": "owner/repo", "commit": "0123456789abcdef0123456789abcdef01234567",
            "skill_path": "skills/demo/SKILL.md", "review_level": "L2",
            "disposition": "L2_STATIC_REVIEW_COMPLETE", "tree_truncated": False,
            "files_indexed": 4, "files_selected": 3, "files_read": 3,
            "file_kind_counts": {"skill_definition": 1, "test": 2},
            "file_evidence": [{"path": "skills/demo/SKILL.md", "kind": "skill_definition", "read": True, "bytes": 120}],
            "mechanism_findings": [], "review_errors": [],
            "capability_claims_not_runtime_verified": True, "runtime_tested": False,
            "source_code_executed": False, "limitations": ["Static only."],
            "reviewed_at": "2026-11-01T00:00:00Z"
        }
        self.assertTrue(validator.is_valid(record))
        record["runtime_tested"] = True
        self.assertFalse(validator.is_valid(record))

    def test_l2_schema_accepts_blocked_truncated_tree_record(self):
        schema = json.loads((ROOT / "schemas" / "l2-review.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        record = {
            "repository": "owner/repo", "commit": "0123456789abcdef0123456789abcdef01234567",
            "skill_path": "SKILL.md", "review_level": "L2", "disposition": "BLOCKED",
            "tree_truncated": True, "files_indexed": 0, "files_selected": 0, "files_read": 0,
            "file_kind_counts": {}, "file_evidence": [], "mechanism_findings": [],
            "review_errors": [{"path": "__repository__", "error": "tree truncated"}],
            "capability_claims_not_runtime_verified": True, "runtime_tested": False,
            "source_code_executed": False, "limitations": ["Blocked before inspection."],
            "reviewed_at": "2026-11-01T00:00:00Z"
        }
        self.assertTrue(validator.is_valid(record))

    def test_l1_review_schema_accepts_and_rejects_records(self):
        schema = json.loads((ROOT / "schemas" / "l1-review.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        record = {
            "repository": "owner/repo", "commit": "0123456789abcdef0123456789abcdef01234567",
            "path": "skills/demo/SKILL.md", "metadata_completeness_score": 90,
            "disposition": "L1_CANDIDATE", "flags": [], "review_level": "L1",
            "limitations": ["Not a runtime test."]
        }
        self.assertTrue(validator.is_valid(record))
        record["metadata_completeness_score"] = 101
        self.assertFalse(validator.is_valid(record))

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
