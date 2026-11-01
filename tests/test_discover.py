import importlib.util
import json
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("discover", ROOT / "scripts" / "discover.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class DiscoveryTests(unittest.TestCase):
    def test_frontmatter(self):
        self.assertEqual(mod.parse_frontmatter("---\nname: test-skill\ndescription: useful tool\n---\nbody"),
                         {"name": "test-skill", "description": "useful tool"})

    def test_no_frontmatter(self):
        self.assertEqual(mod.parse_frontmatter("# plain"), {})

    def test_classification(self):
        cats = json.loads((ROOT / "config" / "categories.json").read_text())
        self.assertIn("directing", mod.classify("Storyboard Builder", "Create cinematic storyboards", "shot composition", cats))

    def test_spdx_detection(self):
        self.assertEqual(mod.detect_spdx("/* SPDX-License-Identifier: MIT */\n"), "MIT")
        self.assertIsNone(mod.detect_spdx("Apache License, Version 2.0"))

    def test_license_scope(self):
        self.assertEqual(mod.license_state({"tree":[{"type":"blob","path":"LICENSE"}]}),
                         ("LICENSED_REVIEW_REQUIRED", "LICENSE"))
        self.assertEqual(mod.license_state({"tree":[{"type":"blob","path":"subdir/LICENSE"}]}),
                         ("LICENSE_SCOPE_UNCLEAR", "subdir/LICENSE"))
        self.assertEqual(mod.license_state({"tree":[]}), ("NO_LICENSE_FOUND", None))

    def test_discovery_records_query_and_seed_failures(self):
        def fake_request(url):
            if "/search/repositories?" in url:
                raise RuntimeError("search unavailable")
            raise RuntimeError("seed unavailable")
        with patch.object(mod, "request_json", side_effect=fake_request):
            found, errors = mod.discover_repositories(
                {"queries": ["film skills"], "seed_repositories": ["owner/repo"]}, 5
            )
        self.assertEqual(found, {})
        self.assertEqual(len(errors), 2)
        self.assertEqual({item.get("query") or item.get("repository") for item in errors},
                         {"film skills", "owner/repo"})

if __name__ == "__main__":
    unittest.main()
