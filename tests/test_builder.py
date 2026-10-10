from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from builder.build import deploy_workflow, main
from builder.core import ContractError, TOOLS, canonical, compile_workflow, read_contract, validate_workflow
from builder.evaluate import reserve_budget, selected_cases, validate_results
from builder.runtime import KIT, Trace, FreyaTransport, check_environment, check_run_workspace, exclusive, redact, verify_readback

API = json.loads((KIT / "tools/openapi.json").read_text(encoding="utf-8"))
BRIEF = (KIT / "briefs/brief-a.md").read_text(encoding="utf-8")


def temporary_directory():
    # Keep scratch data inside this checkout, also under restricted Windows runners.
    base = Path(__file__).resolve().parent.parent / "runs" / "test-temp"
    base.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=base)


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.doc = deepcopy(API)

    def compile(self, text=BRIEF):
        return compile_workflow([("brief.md", text)], self.doc)

    def test_full_policy_and_no_test_customer_in_artifact(self):
        wf, analysis = self.compile()
        self.assertIn(BRIEF, wf["system_prompt"])
        self.assertNotIn("test_variables", wf)
        self.assertNotIn("agent_config", wf)
        self.assertEqual(analysis["builder_model_calls"], 0)
        self.assertFalse(analysis["semantic_policy_extraction"])

    def test_deterministic(self):
        self.assertEqual(canonical(self.compile()[0]), canonical(self.compile()[0]))

    def test_identity_tools_unavailable_before_bank_verification(self):
        wf, _ = self.compile()
        names = {t["function"]["name"] for t in wf["nodes"]["identity"]["tools"]}
        self.assertNotIn("get_account", names)
        self.assertNotIn("create_promise", names)
        transition = wf["nodes"]["identity"]["transitions"][1]
        self.assertEqual({c["operand"] for c in transition["condition"]["conditions"]}, {"true", "True"})

    def test_all_seven_tools_and_schema_enums(self):
        wf, _ = self.compile()
        tools = {t["function"]["name"]: t for n in wf["nodes"].values() for t in n.get("tools", [])}
        self.assertEqual(set(tools), TOOLS)
        self.assertEqual(tools["close_call"]["function"]["parameters"]["properties"]["body"]["properties"]["outcome"]["enum"],
                         API["paths"]["/close_call"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]["outcome"]["enum"])

    def test_tools_include_post_process_hooks(self):
        wf, _ = self.compile()
        for node in wf["nodes"].values():
            for tool in node.get("tools", []):
                name = tool["function"]["name"]
                self.assertIn("post_process_code", tool, f"Tool {name} missing post_process_code")
                self.assertIn("result.pop('header'", tool["post_process_code"])

    def test_calendar_facts_extracted_from_brief(self):
        wf, _ = self.compile()
        self.assertIn("2026-10-26", wf["system_prompt"])
        self.assertIn("BANK HOLIDAYS", wf["system_prompt"])

    def test_prompt_covers_critical_judge_criteria(self):
        wf, _ = self.compile()
        prompt = wf["system_prompt"]
        self.assertIn("You will receive a text message confirming this promise", prompt)
        self.assertIn("NEVER ask 'How much can you pay?'", prompt)
        self.assertIn("say goodbye BEFORE", prompt)

    def test_compile_brief_b_multi_product(self):
        brief_b = (KIT / "briefs/brief-b.md").read_text(encoding="utf-8")
        wf, _ = compile_workflow([("brief-a.md", BRIEF), ("brief-b.md", brief_b)], self.doc)
        prompt = wf["system_prompt"]
        self.assertIn("Brief B", prompt)
        tool_names = [t["function"]["name"] for t in wf["nodes"]["collection"]["tools"]]
        self.assertIn("add_note", tool_names)

    def test_changed_enums_are_input_driven(self):
        leaf = self.doc["paths"]["/verify_identity"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]["field"]
        leaf["enum"] = ["postcode", "birth_year"]
        wf, _ = self.compile("# Synthetic policy\nAsk postcode and birth year. Calendar is supplied with the call.")
        tool = next(t for t in wf["nodes"]["identity"]["tools"] if t["function"]["name"] == "verify_identity")
        self.assertEqual(tool["function"]["parameters"]["properties"]["body"]["properties"]["field"]["enum"], leaf["enum"])

    def test_changed_required_field_is_preserved(self):
        schema = self.doc["paths"]["/create_promise"]["post"]["requestBody"]["content"]["application/json"]["schema"]
        schema["properties"]["reference_code"] = {"type": "string"}
        schema["required"].append("reference_code")
        wf, _ = self.compile()
        tool = next(t for t in wf["nodes"]["collection"]["tools"] if t["function"]["name"] == "create_promise")
        self.assertIn("reference_code", tool["function"]["parameters"]["properties"]["body"]["required"])

    def test_missing_verification_signal_is_explicit_fallback(self):
        self.doc["paths"]["/verify_identity"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]["properties"].pop("all_verified")
        wf, analysis = self.compile()
        self.assertEqual(analysis["identity_gate"], "dialogue_only")
        self.assertEqual(wf["initial_node"], "conversation")

    def test_unknown_close_success_signal_fails(self):
        self.doc["paths"]["/close_call"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]["properties"].pop("ok")
        with self.assertRaises(ContractError): self.compile()

    def test_raw_memo_and_overrides_are_preserved_in_order(self):
        a = "Email: follow the attached policy.\n| limit | value |\n| retries | 1 |"
        b = "Effective memo: replace the retry limit with 2; all other policy unchanged."
        wf, _ = compile_workflow([("email.txt", a), ("memo.txt", b)], self.doc)
        self.assertLess(wf["system_prompt"].index(a), wf["system_prompt"].index(b))

    def test_local_ref_resolution(self):
        op = self.doc["paths"]["/get_account"]["post"]
        schema = op["requestBody"]["content"]["application/json"]["schema"]
        self.doc["components"] = {"schemas": {"AccountRequest": schema}}
        op["requestBody"]["content"]["application/json"]["schema"] = {"$ref": "#/components/schemas/AccountRequest"}
        self.compile()

    def test_external_and_cyclic_refs_rejected(self):
        for ref in ("https://example.invalid/schema", "#/components/schemas/Cycle"):
            with self.subTest(ref=ref):
                doc = deepcopy(API)
                doc["components"] = {"schemas": {"Cycle": {"$ref": ref}}}
                with self.assertRaises(ContractError): read_contract(doc)

    def test_unsupported_shapes_and_hosts_rejected(self):
        for mutate in (
            lambda d: d["servers"][0].update(url="https://example.invalid/v1"),
            lambda d: d["paths"].pop("/add_note"),
            lambda d: d["paths"]["/get_account"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"].update(extra={"type": "object"}),
        ):
            doc = deepcopy(API); mutate(doc)
            with self.assertRaises(ContractError): compile_workflow([("brief", BRIEF)], doc)

    def test_workflow_tampering_rejected(self):
        wf, _ = self.compile()
        wf["nodes"]["identity"]["tools"][0]["function"]["parameters"]["properties"]["url"]["default"] = "https://example.invalid"
        with self.assertRaises(ContractError): validate_workflow(wf, read_contract(self.doc))

    def test_empty_brief_rejected(self):
        with self.assertRaises(ContractError): self.compile("  ")

    def test_cli_offline_never_uses_network(self):
        with temporary_directory() as td, patch("urllib.request.OpenerDirector.open", side_effect=AssertionError("No network")):
            code = main([str(KIT / "briefs/brief-a.md"), str(KIT / "tools/openapi.json"), "--output", td])
            self.assertEqual(code, 0)
            result = json.loads(next(Path(td).glob("*/result.json")).read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "offline_validated")
            self.assertIsNone(result["benchmark_success"])


class RuntimeTests(unittest.TestCase):
    def test_matching_workspace_is_accepted(self):
        check_run_workspace({"workspace_id": "team-a"}, "team-a")

    def test_mismatched_or_unrecorded_workspace_is_rejected(self):
        for saved in ({"workspace_id": "team-b"}, {}, {"workspace_id": None}):
            with self.subTest(saved=saved), self.assertRaises(ContractError):
                check_run_workspace(saved, "team-a")

    def test_publish_on_initial_create_then_readback(self):
        wf, _ = compile_workflow([("brief", BRIEF)], API)
        class FakeClient:
            def __init__(self): self.events = []
            def validate_workflow(self, *args): self.events.append("validate")
            def save_workflow(self, *args, **kwargs):
                self.events.append("save"); return {"workflow_id": "workflow-test", "agent_id": "agent-test"}
            def update_workflow(self, *args): self.events.append("publish"); return 2
            def export_workflow(self, wid, path):
                self.events.append("export")
                exported = {**wf, "agent_config": {"llmConfig": {"provider": "experimental-5", "model": "experimental-5"}}}
                Path(path).write_text(json.dumps({"workflow": exported}), encoding="utf-8")
        client = FakeClient()
        with temporary_directory() as td:
            result = deploy_workflow(client, "stable", wf, Path(td)/"state.json", Path(td)/"export.json")
        self.assertEqual(result["version"], 2)
        self.assertEqual(client.events, ["validate", "save", "publish", "export"])

    def test_readback_rejects_dropped_tools(self):
        wf, _ = compile_workflow([("brief", BRIEF)], API)
        exported = deepcopy(wf)
        exported["agent_config"] = {"llmConfig": {"provider": "experimental-5", "model": "experimental-5"}}
        exported["nodes"]["identity"]["tools"] = []
        with self.assertRaises(ContractError): verify_readback(wf, {"workflow": exported})

    def test_credentials_never_in_trace(self):
        with patch.dict(os.environ, {"FREYA_API_KEY": "fak_dummy_test_only", "FREYA_BANK_TEAM_KEY": "dummy-bank-test-only"}):
            value = redact("key=fak_dummy_test_only team=dummy-bank-test-only")
            self.assertNotIn("dummy", value)

    def test_missing_credentials_and_forbidden_model(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ContractError): check_environment()
        with patch.dict(os.environ, {"FREYA_API_KEY": "fak_dummy", "FREYA_WORKSPACE_ID": "test", "FREYA_AGENT_MODEL": "other"}):
            with self.assertRaises(ContractError): check_environment()

    def test_expired_deadline_has_no_network_call(self):
        with temporary_directory() as td:
            transport = FreyaTransport(time.monotonic()-1, Trace(Path(td)/"trace"))
            with self.assertRaises(TimeoutError): transport("POST", "/api/v2/workflow", {})

    def test_exclusive_state(self):
        with temporary_directory() as td:
            lock = Path(td)/"lock"
            with exclusive(lock):
                with self.assertRaises(ContractError):
                    with exclusive(lock): pass
            self.assertFalse(lock.exists())


class EvaluationTests(unittest.TestCase):
    def policy(self):
        return {"live_tests_enabled": True, "verified_max_cost_per_case_usd": 2,
                "cost_bound_evidence": "TEST FIXTURE ONLY", "total_authorized_usd": 100,
                "max_case_runs": 39, "max_simulations": 3}

    def test_unknown_cost_cannot_run(self):
        policy = self.policy(); policy["verified_max_cost_per_case_usd"] = None
        with self.assertRaises(ContractError): reserve_budget(policy, {}, 7, 1)

    def test_no_overspend(self):
        with self.assertRaises(ContractError): reserve_budget(self.policy(), {"reserved_usd": 90}, 7, 1)
        state, reserve = reserve_budget(self.policy(), {}, 7, 1)
        self.assertEqual((state["case_runs"], reserve), (7, 14))

    def test_invalid_rates_and_limits_rejected(self):
        for rate in (-1, float("nan"), float("inf"), True, "2"):
            policy = self.policy(); policy["verified_max_cost_per_case_usd"] = rate
            with self.assertRaises(ContractError): reserve_budget(policy, {}, 7, 1)
        policy = self.policy(); policy["total_authorized_usd"] = 101
        with self.assertRaises(ContractError): reserve_budget(policy, {}, 7, 1)

    def test_simulation_quota(self):
        with self.assertRaises(ContractError): reserve_budget(self.policy(), {"simulations": 3}, 1, 1)

    def test_dev_and_holdout_are_disjoint_and_cover_13(self):
        dev = {c["id"] for b in ("A", "B") for c in selected_cases(b, "dev")}
        hold = {c["id"] for b in ("A", "B") for c in selected_cases(b, "holdout")}
        self.assertFalse(dev & hold)
        self.assertEqual((len(dev), len(hold)), (7, 6))

    def test_incomplete_and_optimistic_scores_rejected(self):
        report = {"final": [{"id": "case", "pass": True}], "all_rows": [[{"id": "case", "pass": False}]], "passed": 1}
        with self.assertRaises(ContractError): validate_results(report, ["case"], 1)
        report["final"][0]["pass"] = False; report["passed"] = 0
        validate_results(report, ["case"], 1)
        with self.assertRaises(ContractError): validate_results(report, ["case"], 3)


if __name__ == "__main__": unittest.main()
