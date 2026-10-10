from copy import deepcopy
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
import urllib.error
from unittest.mock import patch

from builder.build import deploy_workflow, main
from builder.core import ContractError, TOOLS, canonical, compile_workflow, read_contract, validate_workflow
from builder.evaluate import reserve_budget, selected_cases, validate_results, bounded_simulation_body, retry_ledger_read, call_telemetry
from builder.campaign import check_campaign, reserve_campaign, settle_campaign
from builder.calendar import calendar_code, calendar_spec, deadline_bands, offer_code
from builder.runtime import KIT, Trace, FreyaTransport, check_environment, check_run_workspace, exclusive, redact, verify_readback, verify_key_workspace

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

    def test_calendar_counts_after_today_and_crosses_holiday_year_boundary(self):
        spec = calendar_spec([("policy", "Business days are Monday to Friday, except Example Bank holidays: 2030-01-01.")])
        snippet = calendar_code(spec)
        values = {"now": "2029-12-28T11:00"}
        exec(snippet, {"vars": values})
        facts = values["calendar_facts"]
        self.assertIn("2029-12-31 Monday | business day AFTER today #1", facts)
        self.assertIn("2030-01-01 Tuesday | NON-BUSINESS DAY", facts)
        self.assertIn("2030-01-01 Tuesday | NON-BUSINESS DAY; NEXT BUSINESS DAY = 2030-01-02 Wednesday", facts)
        self.assertIn("2030-01-02 Wednesday | business day AFTER today #2", facts)
        self.assertNotIn("{{", snippet)
        self.assertNotIn("}}", snippet)
        fallback = {"now": "invalid"}
        exec(snippet, {"vars": fallback})
        self.assertIn("unavailable", fallback["calendar_facts"])
        self.assertIsNone(calendar_spec([("policy", "Holidays depend on the account's country.")]))
        self.assertIsNone(calendar_spec([("policy", "Business days are Monday to Friday, except bank holidays: 2030-02-30.")]))

    def test_identity_tools_unavailable_before_bank_verification(self):
        wf, _ = self.compile()
        names = {t["function"]["name"] for t in wf["nodes"]["identity"]["tools"]}
        self.assertNotIn("get_account", names)
        self.assertNotIn("create_promise", names)
        transition = wf["nodes"]["identity"]["transitions"][1]
        self.assertEqual({c["operand"] for c in transition["condition"]["conditions"]}, {"true", "True"})

    def test_offer_calculation_uses_input_bands_and_each_account_product(self):
        policy = "Business days are Monday to Friday, except Example holidays: 2030-01-01.\n| 1 to 9 | early | the 4th business day after today | 1 |\n| 10 to 90 | late | the 2nd business day after today | 2 |"
        briefs = [("policy", policy)]
        values = {"now": "2029-12-28T11:00", "payment_offer_date": "2030-01-01", "payment_offer_action": "resolve",
                  "get_account_response.data.products.0.product_id": "x", "get_account_response.data.products.0.days_late": 3,
                  "get_account_response.data.products.1.product_id": "y", "get_account_response.data.products.1.days_late": 15}
        code = offer_code(calendar_spec(briefs), deadline_bands(briefs))
        exec(code, {"vars": values})
        self.assertEqual(values["payment_offer_action"], "none")
        self.assertIn("DATE TO OFFER FOR THIS PRODUCT: 2030-01-02", values["payment_date_facts"])
        self.assertIn("PRODUCT x: days_late=3; DEADLINE=2030-01-04", values["payment_date_facts"])
        self.assertIn("PRODUCT y: days_late=15; DEADLINE=2030-01-02", values["payment_date_facts"])
        values["payment_offer_date"] = "2030-01-03"
        exec(code, {"vars": values})
        self.assertIn("outside the allowed window", values["payment_date_facts"])
        self.assertNotIn("{{", code)
        self.assertNotIn("}}", code)

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
                # Ensure post_process_code compiles cleanly as valid Python code
                compile(tool["post_process_code"], f"<hook_{name}>", "exec")


    def test_calendar_facts_extracted_from_brief(self):
        wf, _ = self.compile()
        self.assertIn("2026-10-26", wf["system_prompt"])
        self.assertIn("BANK HOLIDAYS", wf["system_prompt"])

    def test_arbitrary_holidays_extracted_from_brief(self):
        synthetic_brief = "Bank policy: holidays are 2026-11-26 and 2026-12-25. Must skip them."
        wf, _ = self.compile(synthetic_brief)
        self.assertIn("2026-11-26, 2026-12-25", wf["system_prompt"])


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
        with self.assertRaises(ContractError):
            self.compile()

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

    def test_openapi_with_null_and_omitted_documentation_fields(self):
        doc = deepcopy(API)
        for path_item in doc["paths"].values():
            op = path_item["post"]
            op["summary"] = None
            op["description"] = None
            for prop in op["requestBody"]["content"]["application/json"]["schema"]["properties"].values():
                prop["description"] = None
        wf, _ = compile_workflow([("brief", BRIEF)], doc)
        self.assertIn("identity", wf["nodes"])
        for tool in wf["nodes"]["identity"]["tools"]:
            self.assertIsInstance(tool["function"]["description"], str)

    def test_calendar_synonyms_and_non_holiday_iso_dates(self):
        brief = ("# Policy\nBusiness days are Monday through Friday, except bank holidays: 2027-04-15.\n"
                 "The call took place on 2027-04-01. Customer was late.\n"
                 "| 1 to 7 | early | the 7th business day after today | 1 |\n"
                 "| 8 to 45 | late | the 7th business day after today | 2 |")
        wf, analysis = compile_workflow([("policy.md", brief)], self.doc)
        self.assertIn("2027-04-15", wf["system_prompt"])
        self.assertNotIn("2027-04-01", analysis["calendar"]["holidays"])

    def test_verify_identity_hook_execution_matrix(self):
        from builder.core import make_post_process_code
        code = make_post_process_code("verify_identity")
        scenarios = [
            ({"data": {"all_verified": True}}, "All security questions PASSED"),
            ({"data": {"verified": True}}, "Date of birth verified"),
            ({"data": {"hint": "day_month_swapped"}}, "Day and month were swapped"),
            ({"data": {"verified": False, "wrong_answers_left": 2}}, "2 attempts left"),
            ({"data": {"verified": False, "wrong_answers_left": 0}}, "Three wrong answers reached"),
            ({"data": {"verified": False}}, "Answer did not match"),
        ]
        for res, expected in scenarios:
            scope = {"result": deepcopy(res)}
            exec(code, scope)
            self.assertIn(expected, scope["result"]["data"].get("what_to_do_next", ""))

    def test_create_promise_hook_execution_matrix(self):
        from builder.core import make_post_process_code
        code = make_post_process_code("create_promise")
        success_scope = {"result": {"data": {"ok": True}}}
        exec(code, success_scope)
        self.assertIn("Payment promise RECORDED", success_scope["result"]["data"]["what_to_do_next"])

        fail_scope = {"result": {"data": {"ok": False}}}
        exec(code, fail_scope)
        self.assertIn("Promise recording FAILED", fail_scope["result"]["data"]["what_to_do_next"])

    def test_deadline_bands_with_dash_and_arbitrary_ranges(self):
        policy = "# Policy\n| 1 - 7 | early | the 5th business day after today |\n| 8 - 30 | late | the 3rd business day after today |"
        bands = deadline_bands([("policy.md", policy)])
        self.assertEqual(bands, [[1, 7, 5], [8, 30, 3]])

    def test_cli_offline_never_uses_network(self):
        with temporary_directory() as td, patch("urllib.request.OpenerDirector.open", side_effect=AssertionError("No network")):
            code = main([str(KIT / "briefs/brief-a.md"), str(KIT / "tools/openapi.json"), "--output", td])
            self.assertEqual(code, 0)
            result = json.loads(next(Path(td).glob("*/result.json")).read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "offline_validated")
            self.assertIsNone(result["benchmark_success"])


class RuntimeTests(unittest.TestCase):
    def test_key_scope_must_match_before_mutations(self):
        for response in ({"workspaces": [{"id": "team-a"}]}, {"items": [{"id": "team-a"}]}, [{"id": "team-a"}]):
            verify_key_workspace(response, "team-a")
        for response in ({}, [], {"workspaces": [{"id": "team-b"}]},
                         {"workspaces": [{"id": "team-a"}, {"id": "team-b"}]}, {"workspaces": [None]}):
            with self.subTest(response=response), self.assertRaises(ContractError):
                verify_key_workspace(response, "team-a")

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

    def test_only_explicit_simulation_conflict_is_waitable(self):
        with temporary_directory() as td, patch.dict(os.environ, {"FREYA_API_KEY": "test-fixture"}):
            trace_path = Path(td) / "trace"
            transport = FreyaTransport(time.monotonic()+30, Trace(trace_path))
            for status, body, expected in ((403, b'{"message":"concurrent simulations limit"}', RuntimeError),
                                           (403, b'{"message":"permission denied"}', ContractError),
                                           (500, b'concurrent simulations', ContractError)):
                error = urllib.error.HTTPError("https://example.invalid", status, "error", {}, io.BytesIO(body))
                with patch.object(transport.opener, "open", side_effect=error):
                    with self.assertRaises(expected): transport("POST", "/api/v2/simulations", {})
            self.assertNotIn("permission denied", trace_path.read_text())

    def test_exclusive_state(self):
        with temporary_directory() as td:
            lock = Path(td)/"lock"
            with exclusive(lock):
                with self.assertRaises(ContractError):
                    with exclusive(lock): pass
            self.assertFalse(lock.exists())


class EvaluationTests(unittest.TestCase):
    def test_tool_exceptions_are_counted_but_rejected_identity_is_not_transport_failure(self):
        events = [{"event": "function_call_error", "function": "verify_identity"},
                  {"event": "function_call_complete", "result": {"status": "success", "data": {"ok": True, "verified": False}}},
                  {"event": "function_call_complete", "result": {"status": "error"}}]
        telemetry = call_telemetry({"messages": [{"role": "system", "message": json.dumps(event)} for event in events]})
        self.assertEqual(telemetry, {"observed_tool_completions": 2, "observed_failed_tool_results": 2})

    def test_transient_ledger_read_retries_but_session_creation_does_not(self):
        from unittest.mock import Mock
        failed = json.JSONDecodeError("upstream HTML", "", 0)
        read = Mock(side_effect=[failed, {"promises": []}])
        with patch("builder.evaluate.time.sleep"):
            self.assertEqual(retry_ledger_read(read, "/v1/practice/ledger/example"), {"promises": []})
        self.assertEqual(read.call_count, 2)
        write = Mock(side_effect=failed)
        with self.assertRaises(json.JSONDecodeError): retry_ledger_read(write, "/v1/practice/sessions", {"case": "example"})
        self.assertEqual(write.call_count, 1)

    def test_monitored_campaign_checks_credit_and_unresolved_jobs(self):
        policy = {"monitored_campaign_authorized": True, "total_authorized_usd": 100,
                  "campaign_stop_balance_usd": 20, "max_case_runs": 84, "max_simulations": 16}
        snapshot = {"creditsLeft": 199, "creditUsdRate": 0.5}
        state = reserve_campaign(policy, {}, snapshot, 7, 3, "run-a")
        self.assertEqual(state["case_runs"], 21)
        self.assertEqual(state["observed_workspace_spend_usd"], 0.5)
        with self.assertRaises(ContractError): reserve_campaign(policy, state, snapshot, 1, 1, "run-b")
        with self.assertRaises(ContractError): settle_campaign(state, snapshot, "run-b")
        settled = settle_campaign(state, {"creditsLeft": 198, "creditUsdRate": 0.5}, "run-a")
        self.assertIsNone(settled["monitored_pending_run"])
        self.assertEqual(settled["observed_workspace_spend_usd"], 1)
        for bad in (0, 39, float("nan"), True):
            with self.assertRaises(ContractError): check_campaign(policy, {"creditsLeft": bad, "creditUsdRate": 0.5}, 7)
        with self.assertRaises(ContractError): check_campaign(policy, snapshot, 8)
        with self.assertRaises(ContractError): check_campaign({**policy, "monitored_campaign_authorized": False}, snapshot, 1)

    def test_credit_pilot_requires_authorization_and_reserves_remaining_budget(self):
        policy = self.policy()
        with self.assertRaises(ContractError): reserve_budget(policy, {}, 1, 1, True)
        policy.update(credit_pilot_authorized=True, live_tests_enabled=False, verified_max_cost_per_case_usd=None)
        state, reserve = reserve_budget(policy, {"other_spend_usd": 2}, 1, 1, True)
        self.assertEqual(reserve, 98)
        self.assertTrue(state["credit_pilot_started"])
        with self.assertRaises(ContractError): reserve_budget(policy, state, 1, 1, True)
        with self.assertRaises(ContractError): reserve_budget(policy, {}, 2, 1, True)
        with self.assertRaises(ContractError): reserve_budget(policy, {}, 1, 2, True)

    def test_simulation_has_no_automatic_retries(self):
        body = {"mode": "chat", "runsPerPersona": 1, "maxRetries": 5, "maxConcurrentCalls": 5, "maxCallDurationSeconds": 420}
        bounded = bounded_simulation_body(body)
        self.assertEqual((bounded["maxRetries"], bounded["maxConcurrentCalls"]), (0, 1))
        self.assertEqual(body["maxRetries"], 5)
        with self.assertRaises(ContractError): bounded_simulation_body({**body, "mode": "voice"})

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

    def test_smoke_subset_cannot_leak_holdout_or_duplicate_cases(self):
        first = selected_cases("A", "dev")[0]["id"]
        held = selected_cases("A", "holdout")[0]["id"]
        self.assertEqual([c["id"] for c in selected_cases("A", "dev", first)], [first])
        for only in (held, first + "," + first, "unknown", "", first + ","):
            with self.subTest(only=only), self.assertRaises(ContractError):
                selected_cases("A", "dev", only)

    def test_incomplete_and_optimistic_scores_rejected(self):
        report = {"final": [{"id": "case", "pass": True}], "all_rows": [[{"id": "case", "pass": False}]], "passed": 1}
        with self.assertRaises(ContractError): validate_results(report, ["case"], 1)
        report["final"][0]["pass"] = False; report["passed"] = 0
        validate_results(report, ["case"], 1)
        with self.assertRaises(ContractError): validate_results(report, ["case"], 3)



class StressTests(unittest.TestCase):
    def test_post_process_hooks_resilient_to_primitive_and_empty_inputs(self):
        from builder.core import TOOLS, make_post_process_code
        for name in TOOLS:
            code = make_post_process_code(name)
            for bad_input in (None, "", 0, 42, [], [1, 2], {}, {"header": {"auth": "secret"}}, {"data": "not-a-dict"}):
                scope = {"result": deepcopy(bad_input)}
                try:
                    exec(code, scope)
                except Exception as e:
                    self.fail(f"Hook {name} crashed on input {bad_input!r}: {e}")
                if isinstance(scope.get("result"), dict):
                    self.assertNotIn("header", scope["result"])

    def test_calendar_code_with_leap_year_and_end_of_year(self):
        spec = calendar_spec([("policy", "Business days are Monday to Friday, except bank holidays: 2028-03-01.")])
        snippet = calendar_code(spec)
        # Leap year leap day: 2028-02-29 is Tuesday
        values = {"now": "2028-02-28T09:00"}
        exec(snippet, {"vars": values})
        facts = values["calendar_facts"]
        self.assertIn("2028-02-29 Tuesday | business day AFTER today #1", facts)
        self.assertIn("2028-03-01 Wednesday | NON-BUSINESS DAY", facts)

    def test_calendar_code_when_now_is_weekend_or_holiday(self):
        spec = calendar_spec([("policy", "Business days are Monday to Friday, except bank holidays: 2026-10-26.")])
        snippet = calendar_code(spec)
        # Saturday now
        values = {"now": "2026-10-24T14:30"}
        exec(snippet, {"vars": values})
        self.assertIn("NON-BUSINESS DAY", values["calendar_facts"])
        self.assertIn("NEXT BUSINESS DAY = 2026-10-27 Tuesday", values["calendar_facts"])

    def test_offer_code_with_single_and_multiple_products(self):
        spec = calendar_spec([("policy", "Business days are Monday to Friday, except bank holidays: 2026-10-26.")])
        bands = [[1, 7, 7], [8, 45, 7]]
        code = offer_code(spec, bands)
        values = {
            "now": "2026-10-14T10:00",
            "payment_offer_date": "2026-10-20",
            "get_account_response.data.products.0.product_id": "p1",
            "get_account_response.data.products.0.days_late": 5,
            "get_account_response.data.products.1.product_id": "p2",
            "get_account_response.data.products.1.days_late": 20,
        }
        exec(code, {"vars": values})
        self.assertEqual(values["payment_offer_action"], "none")
        self.assertIn("PRODUCT p1", values["payment_date_facts"])
        self.assertIn("PRODUCT p2", values["payment_date_facts"])

    def test_offer_code_with_days_late_exceeding_bands(self):
        spec = calendar_spec([("policy", "Business days are Monday to Friday, except bank holidays: 2026-10-26.")])
        bands = [[1, 7, 7], [8, 45, 7]]
        code = offer_code(spec, bands)
        values = {
            "now": "2026-10-14T10:00",
            "payment_offer_date": "2026-10-20",
            "get_account_response.data.products.0.product_id": "p_orphan",
            "get_account_response.data.products.0.days_late": 99,
        }
        exec(code, {"vars": values})
        self.assertIn("deadline not computed; consult policy", values["payment_date_facts"])

    def test_offer_code_malformed_input_graceful_fallback(self):
        spec = calendar_spec([("policy", "Business days are Monday to Friday, except bank holidays: 2026-10-26.")])
        bands = [[1, 7, 7]]
        code = offer_code(spec, bands)
        for bad_date in ("gibberish", "", "2026-99-99", None):
            values = {"now": "2026-10-14T10:00", "payment_offer_date": bad_date}
            exec(code, {"vars": values})
            self.assertEqual(values["payment_offer_action"], "none")
            self.assertIn("unavailable", values["payment_date_facts"])

    def test_compile_with_three_hierarchical_documents(self):
        doc = deepcopy(API)
        p1 = ("policy.md", "# Base Policy\nBusiness days are Monday to Friday, except bank holidays: 2026-10-26.\n"
              "| 1 to 7 | early | the 7th business day after today | 1 |\n")
        p2 = ("amendment.md", "# Amendment 1\nFloor payments allowed for credit cards.\n")
        p3 = ("override.md", "# Branch Memo\nCallbacks accepted between 10:00 and 19:00.\n")
        wf, analysis = compile_workflow([p1, p2, p3], doc)
        self.assertEqual(len(analysis["documents"]), 3)
        self.assertIn("Base Policy", wf["system_prompt"])
        self.assertIn("Amendment 1", wf["system_prompt"])
        self.assertIn("Branch Memo", wf["system_prompt"])

    def test_compile_with_international_characters_and_emojis(self):
        doc = deepcopy(API)
        brief = ("# Bank Brief — Çağrı Merkezi Politikası 💳\n"
                 "Business days are Monday to Friday, except bank holidays: 2026-10-26.\n"
                 "| 1 to 7 | early | the 7th business day after today | 1 |\n"
                 "Müşteri Türkçe ve İngilizce konuşabilir; yanıtlar strictly in English.\n")
        wf, analysis = compile_workflow([("intl.md", brief)], doc)
        self.assertIn("Çağrı Merkezi", wf["system_prompt"])
        self.assertEqual(analysis["documents"][0]["characters"], len(brief))

    def test_openapi_with_various_scalar_types(self):
        doc = deepcopy(API)
        props = doc["paths"]["/add_note"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]
        props["priority"] = {"type": "integer"}
        props["amount"] = {"type": "number"}
        props["flag"] = {"type": "boolean"}
        wf, _ = compile_workflow([("brief", BRIEF)], doc)
        tool = next(t for t in wf["nodes"]["collection"]["tools"] if t["function"]["name"] == "add_note")
        tool_props = tool["function"]["parameters"]["properties"]["body"]["properties"]
        self.assertIn("priority", tool_props)
        self.assertIn("amount", tool_props)
        self.assertIn("flag", tool_props)

    def test_validate_workflow_enforces_isolated_nodes(self):
        wf, _ = compile_workflow([("brief", BRIEF)], API)
        # Inject disconnected island node
        wf["nodes"]["island"] = {
            "name": "island", "node_type": "conversation", "task_message": "lost",
            "tools": [], "transitions": []
        }
        with self.assertRaises(ContractError):
            validate_workflow(wf, read_contract(API))

    def test_read_contract_rejects_non_scalar_properties(self):
        doc = deepcopy(API)
        props = doc["paths"]["/add_note"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]
        props["nested_object"] = {"type": "object", "properties": {"foo": {"type": "string"}}}
        with self.assertRaises(ContractError):
            read_contract(doc)

    def test_read_contract_rejects_array_properties(self):
        doc = deepcopy(API)
        props = doc["paths"]["/add_note"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]
        props["items_list"] = {"type": "array", "items": {"type": "string"}}
        with self.assertRaises(ContractError):
            read_contract(doc)

    def test_generalized_freya_origin_and_working_day_bands(self):
        doc_workers = deepcopy(API)
        doc_workers["servers"][0]["url"] = "https://bank-final.freyavoice.workers.dev"
        contract_workers = read_contract(doc_workers)
        self.assertEqual(contract_workers["get_account"]["url"], "https://bank-final.freyavoice.workers.dev/get_account")

        doc_ai = deepcopy(API)
        doc_ai["servers"][0]["url"] = "https://mock.freyavoice.ai"
        contract_ai = read_contract(doc_ai)
        self.assertEqual(contract_ai["get_account"]["url"], "https://mock.freyavoice.ai/get_account")

        doc_invalid = deepcopy(API)
        doc_invalid["servers"][0]["url"] = "https://malicious-bank.com"
        with self.assertRaises(ContractError):
            read_contract(doc_invalid)

        # Multiple servers accepted, picking the first
        doc_multi = deepcopy(API)
        doc_multi["servers"] = [
            {"url": "https://live.freyavoice.ai", "description": "Production"},
            {"url": "https://sandbox.freyavoice.ai", "description": "Sandbox"}
        ]
        contract_multi = read_contract(doc_multi)
        self.assertEqual(contract_multi["get_account"]["url"], "https://live.freyavoice.ai/get_account")

        # Flexible bands: 'within 7 business days' without 'after today'
        custom_brief = "# Policy\n| 1 to 14 | early | within 10 working days |\n| 15 to 60 | late | 5 business days |"
        bands = deadline_bands([("brief.md", custom_brief)])
        self.assertEqual(bands, [[1, 14, 10], [15, 60, 5]])

    def test_natural_language_holidays_normalized(self):
        from builder.calendar import parse_iso_and_natural_dates
        dates1 = parse_iso_and_natural_dates("Bank holidays: October 26th, 2026, November 11, 2026, and Dec 25, 2026.")
        self.assertEqual(dates1, ["2026-10-26", "2026-11-11", "2026-12-25"])

        dates2 = parse_iso_and_natural_dates("Holidays: 26th of October 2026, 2026/11/15, 2027.01.01")
        self.assertEqual(dates2, ["2026-10-26", "2026-11-15", "2027-01-01"])

        # Alternative phrasing: "Bank holidays to skip:"
        brief = "# Branch Memo\nBank holidays to skip: 26th of October 2026, November 11, 2026."
        spec = calendar_spec([("policy", brief)])
        self.assertIsNotNone(spec)
        self.assertEqual(spec["holidays"], ["2026-10-26", "2026-11-11"])

    def test_offer_code_with_list_of_products_structure(self):
        from builder.calendar import offer_code
        spec = {"holidays": ["2026-10-26"]}
        bands = [[1, 7, 7], [8, 45, 7]]
        code = offer_code(spec, bands)
        values = {
            "now": "2026-10-14T10:00",
            "payment_offer_date": "2026-10-20",
            "get_account_response.data.products": [
                {"product_id": "card_99", "days_late": 4},
                {"product_id": "loan_88", "days_late": 15}
            ]
        }
        exec(code, {"vars": values})
        self.assertEqual(values["payment_offer_action"], "none")
        self.assertIn("PRODUCT card_99", values["payment_date_facts"])
        self.assertIn("PRODUCT loan_88", values["payment_date_facts"])


if __name__ == "__main__": unittest.main()
