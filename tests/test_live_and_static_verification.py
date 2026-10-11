import json
import os
import shutil
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "starter-v3" / "build-the-builder"))
import freya
from builder.build import main
from builder.core import compile_workflow

class LiveAndStaticVerificationTests(unittest.TestCase):
    def test_static_folder_and_mock_url(self):
        out_dir = ROOT / "runs" / "test_folder_static"
        if out_dir.exists():
            shutil.rmtree(out_dir)
        
        main([
            str(ROOT / "starter-v3" / "build-the-builder" / "briefs"),
            "https://hackathon-mock.example.workers.dev",
            "--output", str(out_dir)
        ])
        
        wf_files = list(out_dir.glob("*/workflow.local.json"))
        self.assertTrue(len(wf_files) > 0, "workflow.local.json not found in output directory")
        wf_path = wf_files[0]
        self.assertTrue(wf_path.exists())
        wf = json.loads(wf_path.read_text(encoding="utf-8"))
        
        # Check tools have rewritten mock URL
        nodes = list(wf.get("nodes", {}).values())
        tools = [t for n in nodes for t in n.get("tools", [])]
        self.assertTrue(len(tools) > 0)
        for t in tools:
            tool_url = t["function"]["parameters"]["properties"]["url"]["default"]
            self.assertTrue(
                tool_url.startswith("https://hackathon-mock.example.workers.dev"),
                f"URL not rewritten: {tool_url}"
            )
            
        # Check edge-case prompts in task_message
        all_prompts = " ".join(n.get("task_message", "") for n in nodes)
        self.assertIn("DISTRACTOR DATES", all_prompts)
        self.assertIn("MULTI-TURN DATES", all_prompts)
        self.assertIn("SALARY / PAYDAY OFFERS", all_prompts)
        self.assertIn("OBJECTIONS & QUESTIONS", all_prompts)

    def test_freya_workflow_validation(self):
        # Validate that the generated workflow adheres to Freya schema
        briefs = [(
            "brief-a.md",
            (ROOT / "starter-v3" / "build-the-builder" / "briefs" / "brief-a.md").read_text(encoding="utf-8")
        )]
        doc = json.loads((ROOT / "starter-v3" / "build-the-builder" / "tools" / "openapi.json").read_text(encoding="utf-8"))
        doc["servers"] = [{"url": "https://hackathon-mock.example.workers.dev"}]
        
        wf, analysis = compile_workflow(briefs, doc)
        
        # Test locally using freya.validate_workflow if credentials available
        key_path = ROOT / "state" / "freya-api-key"
        if key_path.exists() and key_path.read_text().strip():
            os.environ["FREYA_API_KEY"] = key_path.read_text().strip()
            freya.HEADERS["Authorization"] = "Bearer " + os.environ["FREYA_API_KEY"]
            val_res = freya.validate_workflow("static_check", wf)
            self.assertTrue(val_res.get("valid", False))
            print("[Freya Live Validation] Live workflow dryRun validation PASSED on Freya staging API!")

if __name__ == "__main__":
    import os
    unittest.main()
