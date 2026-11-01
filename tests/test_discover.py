import importlib.util
import json
import unittest
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

if __name__ == "__main__":
    unittest.main()
