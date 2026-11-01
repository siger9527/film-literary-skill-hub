import importlib.util, json, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("discover",Path(__file__).parents[1]/"scripts"/"discover.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class DiscoveryTests(unittest.TestCase):
    def test_frontmatter(self):
        self.assertEqual(mod.parse_frontmatter("---\nname: test-skill\ndescription: useful tool\n---\nbody"),{"name":"test-skill","description":"useful tool"})
    def test_no_frontmatter(self):
        self.assertEqual(mod.parse_frontmatter("# plain"),{})
    def test_classification(self):
        cats=json.loads((Path(__file__).parents[1]/"config"/"categories.json").read_text())
        result=mod.classify("Storyboard Builder","Create cinematic storyboards","shot composition",cats)
        self.assertIn("directing",result)
if __name__=="__main__": unittest.main()
