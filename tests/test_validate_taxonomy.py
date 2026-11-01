import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_taxonomy", ROOT / "scripts/validate_taxonomy.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class TaxonomyValidatorTests(unittest.TestCase):
    def test_repository_taxonomy_passes(self):
        self.assertTrue(validator.validate(ROOT).startswith("PASS:"))

    def test_rejects_missing_board(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            import shutil
            shutil.copytree(ROOT / "config", target / "config")
            shutil.copytree(ROOT / "catalog", target / "catalog")
            shutil.copytree(ROOT / "library", target / "library")
            boards = sorted((target / "library/21-nodes").glob("00-*/README.md"))
            boards[0].unlink()
            with self.assertRaisesRegex(ValueError, "exactly 21 board"):
                validator.validate(target)

    def test_rejects_stage_boundary_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            import shutil
            shutil.copytree(ROOT / "config", target / "config")
            shutil.copytree(ROOT / "catalog", target / "catalog")
            shutil.copytree(ROOT / "library", target / "library")
            import json
            path = target / "config/categories.json"
            config = json.loads(path.read_text(encoding="utf-8"))
            config["stages"][0]["nodes"].append("03")
            path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "stage definitions"):
                validator.validate(target)

    def test_rejects_broken_knowledge_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            import shutil, json
            shutil.copytree(ROOT / "config", target / "config")
            shutil.copytree(ROOT / "catalog", target / "catalog")
            shutil.copytree(ROOT / "library", target / "library")
            path = target / "catalog/film-production-21-node-index.json"
            index = json.loads(path.read_text(encoding="utf-8"))
            index["nodes"][1]["knowledge_entry_paths"] = ["knowledge-base/does-not-exist.md"]
            path.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing knowledge entry"):
                validator.validate(target)

if __name__ == "__main__":
    unittest.main()
