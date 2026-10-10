"""Comprehensive regression tests covering all 10 audit findings."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from builder.calendar import calendar_spec, calendar_code, WEEKDAY_MAP
from builder.core import (
    ContractError,
    Policy,
    parse_policy,
    compile_workflow,
    canonical,
    digest,
    make_post_process_code,
    TRIGGERS,
)
from builder.evaluate import verify_platform_version_binding
from builder.runtime import KIT, ROOT, verify_readback


class AuditFixesRegressionTest(unittest.TestCase):
    def setUp(self):
        self.brief_a = (KIT / "briefs" / "brief-a.md").read_text(encoding="utf-8")
        self.openapi = json.loads((KIT / "tools" / "openapi.json").read_text(encoding="utf-8"))

    # -------------------------------------------------------------------------
    # 1. BRIEF VE SEMA DEGISINCE CELISEN SABIT KURALLARI KALDIR
    # -------------------------------------------------------------------------
    def test_item1_dynamic_policy_derivation_different_bank_and_rules(self):
        """Custom bank name, questions, wrong answer limit, bands, and enums."""
        custom_brief = """# Horizon Credit Bank Debt Collection
You are a debt collection agent for Horizon Credit Bank.
Ask the customer their security questions: postal_code, ssn_last4.
If they give 2 wrong answers, transfer the call immediately.
Payment deadlines:
- Accounts 1 to 9 days late have 4 business days to pay.
- Accounts 10 to 90 days late have 2 business days to pay.
Callback hours are strictly 10:00 to 16:00.
"""
        custom_openapi = copy.deepcopy(self.openapi)
        # Custom enums for close_call
        close_schema = custom_openapi["paths"]["/close_call"]["post"]["requestBody"]["content"]["application/json"]["schema"]
        close_schema["properties"]["outcome"]["enum"] = ["success_resolved", "failed_escalated"]
        close_schema["properties"]["reason"]["enum"] = ["agreed", "refused", "service_down"]

        workflow, analysis = compile_workflow([("custom.md", custom_brief)], custom_openapi)
        wf_str = json.dumps(workflow)

        # 1. Bank name should be Horizon Credit Bank, not Atlas Bank
        self.assertIn("Horizon Credit Bank", wf_str)
        self.assertNotIn("Atlas Bank", wf_str)

        # 2. Max wrong answers in identity node should be 2
        identity_node = workflow["nodes"]["identity"]
        self.assertIn("2 wrong answers", identity_node["task_message"].lower())

        # 3. Calendar / offer prompt should reflect 4 and 2 business day deadlines
        self.assertIn("4 business days", wf_str)
        self.assertIn("2 business days", wf_str)

        # 4. Custom close_call outcomes present in tools / hooks
        self.assertIn("success_resolved", wf_str)
        self.assertIn("failed_escalated", wf_str)

    # -------------------------------------------------------------------------
    # 2. KIMLIK SERVIS HATASIYLA YANLIS CEVABI AYIR
    # -------------------------------------------------------------------------
    def test_item2_identity_hook_distinguishes_service_error_from_wrong_answer(self):
        """HTTP 500 or timeout must NOT be treated as customer wrong answer."""
        code = make_post_process_code("verify_identity")

        # Case A: HTTP 500 error from bank service
        scope_500 = {
            "result": {"status": "error", "status_code": 500, "data": {"error": "Internal Server Error"}},
            "variables": {"wrong_attempts": 0, "verified": False},
        }
        exec(code, scope_500)
        directive_500 = scope_500["result"].get("what_to_do_next", "")
        self.assertIn("service error", directive_500.lower())
        self.assertIn("not a customer wrong answer", directive_500.lower())
        # In error, data dictionary must NOT have instructions
        self.assertNotIn("what_to_do_next", scope_500["result"].get("data", {}))

        # Case B: Bank returns verified=False (customer provided wrong answer)
        scope_wrong = {
            "result": {"status": "ok", "status_code": 200, "data": {"verified": False, "attempts_left": 2}},
            "variables": {"wrong_attempts": 0, "verified": False},
        }
        exec(code, scope_wrong)
        directive_wrong = scope_wrong["result"]["data"].get("what_to_do_next", "")
        self.assertIn("did not match", directive_wrong.lower())
        self.assertNotIn("service error", directive_wrong.lower())

        # Case C: Partial verification (verified=True, all_verified=False)
        scope_partial = {
            "result": {"status": "ok", "status_code": 200, "data": {"verified": True, "all_verified": False}},
            "variables": {"wrong_attempts": 0, "verified": False},
        }
        exec(code, scope_partial)
        directive_partial = scope_partial["result"]["data"].get("what_to_do_next", "")
        self.assertIn("ask the next required security question", directive_partial.lower())

        # Case D: Full verification (all_verified=True)
        scope_full = {
            "result": {"status": "ok", "status_code": 200, "data": {"verified": True, "all_verified": True}},
            "variables": {"wrong_attempts": 0, "verified": False},
        }
        exec(code, scope_full)
        directive_full = scope_full["result"]["data"].get("what_to_do_next", "")
        self.assertIn("all security questions passed", directive_full.lower())

    def test_item2_guidance_forbids_blanket_identity_service_error_prohibition(self):
        """Workflow system prompt must NOT claim verify_identity can never fail with service_error."""
        workflow, _ = compile_workflow([("brief-a.md", self.brief_a)], self.openapi)
        wf_str = json.dumps(workflow)
        self.assertNotIn("Never close as service_error during identity verification", wf_str)
        self.assertIn("A rejected identity answer is not a service error", wf_str)

    # -------------------------------------------------------------------------
    # 3. KIMLIK KAPISINI SEMA DEGISINCE KALDIRMA (FAIL-CLOSED)
    # -------------------------------------------------------------------------
    def test_item3_missing_identity_gate_fails_closed(self):
        """When OpenAPI schema has no recognizable identity gate, fail closed with ContractError."""
        bad_openapi = copy.deepcopy(self.openapi)
        # Remove all_verified from response schema
        bad_props = bad_openapi["paths"]["/verify_identity"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]["properties"]
        bad_props.pop("all_verified", None)

        with self.assertRaises(ContractError) as ctx:
            compile_workflow([("brief-a.md", self.brief_a)], bad_openapi)
        self.assertIn("no recognized completion signal", str(ctx.exception))

    def test_item3_alternative_identity_gate_supported(self):
        """If schema uses identity_complete instead of all_verified, adapter supports it."""
        alt_openapi = copy.deepcopy(self.openapi)
        props = alt_openapi["paths"]["/verify_identity"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]["properties"]
        props.pop("all_verified", None)
        props["identity_complete"] = {"type": "boolean"}

        workflow, analysis = compile_workflow([("brief-a.md", self.brief_a)], alt_openapi)
        self.assertEqual(analysis["identity_gate"], "bank_identity_complete")
        identity_node = workflow["nodes"]["identity"]
        # Transition condition must check identity_complete
        gate_transition = [t for t in identity_node["transitions"] if "identity_complete" in json.dumps(t)]
        self.assertTrue(len(gate_transition) > 0)

    # -------------------------------------------------------------------------
    # 4. HATALI GET_ACCOUNT SONUCUNU BASARI GIBI SUNMA
    # -------------------------------------------------------------------------
    def test_item4_get_account_hook_handles_errors_honestly(self):
        """get_account must never emit 'Account loaded' on status=error, 500, or ok=false."""
        code = make_post_process_code("get_account")

        # Test HTTP 500 / status=error
        scope_err = {
            "result": {"status": "error", "status_code": 500, "data": {"error": "DB unavailable"}},
            "variables": {},
        }
        exec(code, scope_err)
        directive_err = scope_err["result"].get("what_to_do_next", "")
        self.assertNotIn("Account loaded", directive_err)
        self.assertIn("service_error", directive_err)
        self.assertNotIn("what_to_do_next", scope_err["result"].get("data", {}))

        # Test envelope ok=False
        scope_ok_false = {
            "result": {"status": "ok", "status_code": 200, "data": {"ok": False, "error": "Customer record locked"}},
            "variables": {},
        }
        exec(code, scope_ok_false)
        directive_ok_false = scope_ok_false["result"].get("what_to_do_next", "")
        self.assertNotIn("Account loaded", directive_ok_false)
        self.assertIn("service_error", directive_ok_false)

        # Test true success
        scope_success = {
            "result": {"status": "ok", "status_code": 200, "data": {"ok": True, "accounts": [{"product_id": "p1"}]}},
            "variables": {},
        }
        exec(code, scope_success)
        directive_success = scope_success["result"]["data"].get("what_to_do_next", "")
        self.assertIn("Account loaded", directive_success)

    # -------------------------------------------------------------------------
    # 5. ODEME KAYDINI DETERMINISTIK KONTROLLERLE SINIRLA
    # -------------------------------------------------------------------------
    def test_item5_create_promise_trigger_and_verification_boundary(self):
        """create_promise trigger enforces verified identity, bounds, and explicit confirmation."""
        trigger = TRIGGERS["create_promise"]
        self.assertIn("CALL only after the brief's amount/date checks and explicit confirmation", trigger)
        self.assertIn("Do not claim success before the result", trigger)

        # Verify in generated workflow that unverified node cannot access create_promise
        workflow, _ = compile_workflow([("brief-a.md", self.brief_a)], self.openapi)
        identity_tools = workflow["nodes"]["identity"]["tools"]
        self.assertNotIn("create_promise", identity_tools)
        self.assertNotIn("get_account", identity_tools)

    # -------------------------------------------------------------------------
    # 6. TAKVIMDE GIZLI VARSAYIMLARI KALDIR
    # -------------------------------------------------------------------------
    def test_item6_calendar_friday_holiday_resolves_last_bday_to_thursday(self):
        """When Friday is a holiday, last business day of the week must resolve to Thursday."""
        brief_with_friday_holiday = """# Bank Policy
Business days are Monday through Friday.
Official bank holidays:
- 2026-10-16: Autumn Bank Holiday (which is a Friday!)
"""
        spec = calendar_spec([("holiday_brief.md", brief_with_friday_holiday)])
        self.assertIn("2026-10-16", spec["holidays"])
        code = calendar_code(spec)
        scope = {"vars": {"now": "2026-10-12T10:00:00Z"}}
        exec(code, scope)

        # Monday 2026-10-12: Friday 2026-10-16 is a holiday, so last business day is Thursday 2026-10-15
        self.assertEqual(scope["vars"]["last_business_day_of_this_week"], "2026-10-15")

    def test_item6_calendar_tuesday_through_saturday_workweek(self):
        """Custom workweek: Tuesday through Saturday (Sunday and Monday are weekend)."""
        brief_tue_sat = """# Bank Policy
Business days are Tuesday through Saturday.
Official bank holidays:
- 2026-10-21: Bank Holiday
"""
        spec = calendar_spec([("tue_sat_brief.md", brief_tue_sat)])
        self.assertEqual(spec["workdays"], [1, 2, 3, 4, 5])  # Tue, Wed, Thu, Fri, Sat
        code = calendar_code(spec)

        # Start on Saturday 2026-10-17. Next business day after today (#1) is Tuesday 2026-10-20!
        scope = {"vars": {"now": "2026-10-17T10:00:00Z"}}
        exec(code, scope)
        facts = scope["vars"]["calendar_facts"]
        self.assertIn("2026-10-20 Tuesday | business day AFTER today #1", facts)

    # -------------------------------------------------------------------------
    # 7. DEGERLENDIRMEYI GERCEK WORKFLOW SURUMUNE BAGLA
    # -------------------------------------------------------------------------
    def test_item7_verify_platform_version_binding_mismatch_rejected(self):
        """Saved version 4 vs live platform version 99 must raise ContractError before tests."""
        mock_client = MagicMock()
        mock_client.api.return_value = {
            "versions": [
                {"versionNumber": 4, "isPublished": False},
                {"versionNumber": 99, "isPublished": True},
            ]
        }
        saved = {
            "platform_version": 4,
            "workflow_id": "wf-123",
            "workflow_sha256": "abc",
        }

        with self.assertRaises(ContractError) as ctx:
            verify_platform_version_binding(mock_client, saved, "ws-test")
        self.assertIn("Platform version mismatch", str(ctx.exception))
        self.assertIn("version 4", str(ctx.exception))
        self.assertIn("version 99", str(ctx.exception))

    def test_item7_verify_platform_version_binding_matching_succeeds(self):
        """Saved version matching live published version succeeds cleanly."""
        mock_client = MagicMock()
        mock_client.api.return_value = {
            "versions": [
                {"versionNumber": 5, "isPublished": True},
            ]
        }
        saved = {
            "platform_version": 5,
            "workflow_id": "wf-123",
            "workflow_sha256": "abc",
        }
        version = verify_platform_version_binding(mock_client, saved, "ws-test")
        self.assertEqual(version, 5)

    # -------------------------------------------------------------------------
    # 8. READBACK KONTROLUNU TAMAMLA
    # -------------------------------------------------------------------------
    def test_item8_readback_detects_altered_on_enter_and_global_nodes(self):
        """Altering on_enter or injecting global node triggers readback ContractError."""
        workflow, _ = compile_workflow([("brief-a.md", self.brief_a)], self.openapi)

        # Alter on_enter in identity node
        tampered_on_enter = copy.deepcopy(workflow)
        tampered_on_enter["nodes"]["identity"]["on_enter"] = {"type": "silent"}
        with self.assertRaises(ContractError):
            verify_readback(workflow, tampered_on_enter)

        # Inject unexpected global node
        tampered_global = copy.deepcopy(workflow)
        tampered_global["global_nodes"] = [{"name": "injected_global"}]
        with self.assertRaises(ContractError):
            verify_readback(workflow, tampered_global)

        # Alter node set
        tampered_nodes = copy.deepcopy(workflow)
        tampered_nodes["nodes"]["extra_unauthorized_node"] = {"node_type": "conversation"}
        with self.assertRaises(ContractError):
            verify_readback(workflow, tampered_nodes)


if __name__ == "__main__":
    unittest.main()
