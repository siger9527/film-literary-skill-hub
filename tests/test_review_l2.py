import importlib.util
import unittest
ROOT=__import__("pathlib").Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location("review_l2",ROOT/"scripts"/"review_l2.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class L2StaticReviewTests(unittest.TestCase):
    def test_file_classification(self):
        self.assertEqual(mod.classify_file("skills/demo/SKILL.md"),"skill_definition")
        self.assertEqual(mod.classify_file("tests/test_flow.py"),"test")
        self.assertEqual(mod.classify_file("requirements.txt"),"dependency_manifest")
    def test_static_mechanism_signals(self):
        findings=mod.inspect_text("x.py","import subprocess\nsubprocess.run(cmd)\nos.system('x')\neval(code)")
        codes={x["code"] for x in findings}
        self.assertIn("SUBPROCESS_EXECUTION",codes)
        self.assertIn("SHELL_EXECUTION",codes)
        self.assertIn("DYNAMIC_CODE_EXECUTION",codes)
    def test_no_signal_is_not_security_certification(self):
        findings=mod.inspect_text("x.py","def hello(): return 'safe'")
        self.assertEqual(findings,[])
if __name__=="__main__": unittest.main()
