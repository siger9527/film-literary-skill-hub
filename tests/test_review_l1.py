import importlib.util
import unittest
import datetime as dt

ROOT = __import__("pathlib").Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("review_l1", ROOT / "scripts" / "review_l1.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class L1ReviewTests(unittest.TestCase):
    def card(self):
        return {
            "repository":"owner/repo","commit":"0123456789abcdef0123456789abcdef01234567",
            "path":"skills/demo/SKILL.md","source_text_read":True,
            "frontmatter_name_present":True,"frontmatter_description_present":True,
            "readme_present":True,"repository_archived":False,
            "license_status":"LICENSED_REVIEW_REQUIRED",
            "repository_pushed_at":"2026-10-01T00:00:00Z"
        }

    def test_complete_metadata_is_candidate_not_endorsement(self):
        result = mod.assess(self.card(), today=dt.date(2026, 11, 1))
        self.assertEqual(result["disposition"], "L1_CANDIDATE")
        self.assertEqual(result["metadata_completeness_score"], 100)
        self.assertTrue(any("does not measure Skill effectiveness" in x for x in result["limitations"]))

    def test_unreadable_source_is_blocked(self):
        card = self.card()
        card["source_text_read"] = False
        result = mod.assess(card, today=dt.date(2026, 11, 1))
        self.assertEqual(result["disposition"], "BLOCKED")
        self.assertIn("SOURCE_UNREADABLE", result["flags"])

    def test_archived_or_unlicensed_requires_manual_review(self):
        card = self.card()
        card["repository_archived"] = True
        result = mod.assess(card, today=dt.date(2026, 11, 1))
        self.assertEqual(result["disposition"], "MANUAL_REVIEW_REQUIRED")

    def test_stale_repository_is_flagged(self):
        card = self.card()
        card["repository_pushed_at"] = "2024-01-01T00:00:00Z"
        result = mod.assess(card, today=dt.date(2026, 11, 1))
        self.assertIn("REPOSITORY_STALE_OVER_2Y", result["flags"])

if __name__ == "__main__":
    unittest.main()
