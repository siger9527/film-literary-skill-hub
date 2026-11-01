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
    def test_truncated_tree_is_explicitly_blocked(self):
        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self): return b'{"truncated": true, "tree": []}'
        from unittest.mock import patch
        with patch.object(mod.urllib.request, "urlopen", return_value=FakeResponse()):
            with self.assertRaises(mod.ReviewBlocked) as ctx:
                mod.review_resource({"repository":"owner/repo","commit":"0123456789abcdef0123456789abcdef01234567","path":"SKILL.md"})
        self.assertTrue(ctx.exception.tree_truncated)

    def test_no_signal_is_not_security_certification(self):
        findings=mod.inspect_text("x.py","def hello(): return 'safe'")
        self.assertEqual(findings,[])
if __name__=="__main__": unittest.main()
