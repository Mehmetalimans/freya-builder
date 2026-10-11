import json
from pathlib import Path
import unittest

from builder.core import compile_workflow

ROOT = Path(__file__).resolve().parent.parent
OPENAPI_PATH = ROOT / "starter-v3" / "build-the-builder" / "tools" / "openapi.json"


class TestBriefCDEMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.openapi = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
        cls.brief_c = (ROOT / "briefs" / "brief-c.md").read_text(encoding="utf-8")
        cls.brief_d = (ROOT / "briefs" / "brief-d.md").read_text(encoding="utf-8")
        cls.brief_e = (ROOT / "briefs" / "brief-e.md").read_text(encoding="utf-8")

    def test_brief_c_compilation_and_policy(self):
        """Test Brief C (Anatolia Global Bank, 14/5 business day bands, 3 wrong answers)."""
        workflow, analysis = compile_workflow([("brief-c.md", self.brief_c)], self.openapi)
        policy = analysis.get("policy", {})

        self.assertEqual(policy.get("bank_name"), "Anatolia Global Bank")
        self.assertEqual(policy.get("max_wrong_answers"), 3)
        self.assertEqual(policy.get("bands"), [[1, 10, 14], [11, 60, 5]])
        self.assertIn("restructuring", policy.get("transfer_queues", []))

        # Workflow structure
        nodes = workflow["nodes"]
        self.assertEqual(len(nodes), 6)
        self.assertIn("identity", nodes)
        self.assertIn("collection", nodes)

        # Check prompt does not contain old hardcoded bank name
        system_prompt = workflow["system_prompt"]
        self.assertIn("Anatolia Global Bank", system_prompt)
        self.assertNotIn("Freya Bank", system_prompt)

    def test_brief_d_compilation_and_policy(self):
        """Test Brief D (Apex Commercial Finance, 8/3 bands, 2 wrong answers, corporate fields)."""
        custom_openapi = json.loads(json.dumps(self.openapi))
        transfer_props = custom_openapi["paths"]["/transfer_to_agent"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]
        transfer_props["queue"]["enum"] = ["commercial_legal", "factoring_support", "general"]

        workflow, analysis = compile_workflow([("brief-d.md", self.brief_d)], custom_openapi)
        policy = analysis.get("policy", {})

        self.assertEqual(policy.get("bank_name"), "Apex Commercial Finance")
        self.assertEqual(policy.get("max_wrong_answers"), 2)
        self.assertEqual(policy.get("bands"), [[1, 14, 8], [15, 45, 3]])
        self.assertIn("commercial_legal", policy.get("transfer_queues", []))
        self.assertIn("factoring_support", policy.get("transfer_queues", []))

        # Check prompt reflects commercial rules and 2 attempts
        system_prompt = workflow["system_prompt"]
        self.assertIn("Apex Commercial Finance", system_prompt)
        self.assertNotIn("Freya Bank", system_prompt)

    def test_brief_e_compilation_and_policy(self):
        """Test Brief E (Nordic Trust Financial, 4/2 bands, 1 wrong answer, micro-credit)."""
        custom_openapi = json.loads(json.dumps(self.openapi))
        transfer_props = custom_openapi["paths"]["/transfer_to_agent"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]
        transfer_props["queue"]["enum"] = ["special_care", "debt_counseling", "general"]

        workflow, analysis = compile_workflow([("brief-e.md", self.brief_e)], custom_openapi)
        policy = analysis.get("policy", {})

        self.assertEqual(policy.get("bank_name"), "Nordic Trust Financial")
        self.assertEqual(policy.get("max_wrong_answers"), 1)
        self.assertEqual(policy.get("bands"), [[1, 5, 4], [6, 30, 2]])
        self.assertIn("special_care", policy.get("transfer_queues", []))
        self.assertIn("debt_counseling", policy.get("transfer_queues", []))

        # Check prompt reflects rapid micro-credit deadlines
        system_prompt = workflow["system_prompt"]
        self.assertIn("Nordic Trust Financial", system_prompt)
        self.assertNotIn("Freya Bank", system_prompt)

    def test_diverse_case_policy_adaptation(self):
        """Verify that policies dynamically adapt across all 5 briefs (A, B, C, D, E)."""
        brief_a = (ROOT / "starter-v3" / "build-the-builder" / "briefs" / "brief-a.md").read_text(encoding="utf-8")
        brief_b = (ROOT / "starter-v3" / "build-the-builder" / "briefs" / "brief-b.md").read_text(encoding="utf-8")

        _, a_analysis = compile_workflow([("brief-a.md", brief_a)], self.openapi)
        _, b_analysis = compile_workflow([("brief-b.md", brief_b)], self.openapi)
        _, c_analysis = compile_workflow([("brief-c.md", self.brief_c)], self.openapi)
        _, d_analysis = compile_workflow([("brief-d.md", self.brief_d)], self.openapi)
        _, e_analysis = compile_workflow([("brief-e.md", self.brief_e)], self.openapi)

        # Bands comparison across all 5 briefs
        self.assertEqual(a_analysis["policy"]["bands"], [[1, 7, 12], [8, 45, 7]])
        self.assertEqual(b_analysis["policy"]["bands"], [[1, 7, 12], [8, 45, 7]])
        self.assertEqual(c_analysis["policy"]["bands"], [[1, 10, 14], [11, 60, 5]])
        self.assertEqual(d_analysis["policy"]["bands"], [[1, 14, 8], [15, 45, 3]])
        self.assertEqual(e_analysis["policy"]["bands"], [[1, 5, 4], [6, 30, 2]])

        # Wrong answers comparison across all 5 briefs
        self.assertEqual(a_analysis["policy"]["max_wrong_answers"], 3)
        self.assertEqual(b_analysis["policy"]["max_wrong_answers"], 3)
        self.assertEqual(c_analysis["policy"]["max_wrong_answers"], 3)
        self.assertEqual(d_analysis["policy"]["max_wrong_answers"], 2)
        self.assertEqual(e_analysis["policy"]["max_wrong_answers"], 1)

        # Bank names comparison across all 5 briefs
        self.assertEqual(a_analysis["policy"]["bank_name"], "Freya Bank")
        self.assertEqual(b_analysis["policy"]["bank_name"], "Freya Bank")
        self.assertEqual(c_analysis["policy"]["bank_name"], "Anatolia Global Bank")
        self.assertEqual(d_analysis["policy"]["bank_name"], "Apex Commercial Finance")
        self.assertEqual(e_analysis["policy"]["bank_name"], "Nordic Trust Financial")


if __name__ == "__main__":
    unittest.main()
