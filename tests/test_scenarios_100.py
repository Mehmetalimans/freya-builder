"""100-Case Realistic Banking Collections Scenario Test Matrix.

Covers 10 distinct operational categories across realistic debt-recovery calling:
- Category 1 (001-010): Identity, Right-Party Contact (RPC) & Compliance
- Category 2 (011-020): Early Arrears (1-7 Days Late) & First-Contact Resolution
- Category 3 (021-030): Mid & Late Arrears (8-45 Days Late) & Mandatory Floor Negotiations
- Category 4 (031-040): Calendar Arithmetic, Weekend Shifts & Bank Holiday Resolution
- Category 5 (041-050): Boundary Limits, Deadline Constraints & Late Date Enforcements
- Category 6 (051-060): Vulnerability, Hardship, Bereavement & Healthcare Protocols
- Category 7 (061-070): Debt Disputes, Fraud, Bankruptcy & Already-Paid Verifications
- Category 8 (071-080): Escalations, Human Agent Demands & De-escalation Paths
- Category 9 (081-090): Multi-Product Cascades (Brief B), Order Preservation & Notes
- Category 10 (091-100): Conversational Noise, Self-Corrections & System Fault Resiliency
"""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from builder.core import compile_workflow, make_post_process_code, read_contract
from builder.calendar import calendar_spec, calendar_code, deadline_bands, offer_code

KIT = Path(__file__).resolve().parent.parent / "starter-v3" / "build-the-builder"
API = json.loads((KIT / "tools/openapi.json").read_text(encoding="utf-8"))
BRIEF_A = (KIT / "briefs/brief-a.md").read_text(encoding="utf-8")
BRIEF_B = (KIT / "briefs/brief-b.md").read_text(encoding="utf-8")


class HundredScenariosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wf_a, cls.analysis_a = compile_workflow([("brief-a.md", BRIEF_A)], API)
        cls.wf_b, cls.analysis_b = compile_workflow([("brief-a.md", BRIEF_A), ("brief-b.md", BRIEF_B)], API)
        cls.prompt_a = cls.wf_a["system_prompt"]
        cls.prompt_b = cls.wf_b["system_prompt"]
        cls.all_text_a = cls.prompt_a + "\n" + "\n".join(n.get("task_message", "") for n in cls.wf_a["nodes"].values())
        cls.all_text_b = cls.prompt_b + "\n" + "\n".join(n.get("task_message", "") for n in cls.wf_b["nodes"].values())
        cls.cal_spec = calendar_spec([("brief-a.md", BRIEF_A)])
        cls.bands = deadline_bands([("brief-a.md", BRIEF_A)])

    # =========================================================================
    # Category 1: Identity, Right-Party Contact (RPC) & Compliance (001 - 010)
    # =========================================================================

    def test_001_rpc_standard_happy_path(self):
        code = make_post_process_code("verify_identity")
        scope = {"result": {"data": {"verified": True, "all_verified": True}}}
        exec(code, scope)
        self.assertIn("All security questions PASSED", scope["result"]["data"]["what_to_do_next"])

    def test_002_rpc_day_month_swapped_grace_retry(self):
        code = make_post_process_code("verify_identity")
        scope = {"result": {"data": {"hint": "day_month_swapped", "verified": False}}}
        exec(code, scope)
        self.assertIn("Day and month were swapped", scope["result"]["data"]["what_to_do_next"])
        self.assertIn("does NOT count as a wrong answer", scope["result"]["data"]["what_to_do_next"])

    def test_003_rpc_first_wrong_attempt_tracks_attempts_left(self):
        code = make_post_process_code("verify_identity")
        scope = {"result": {"data": {"verified": False, "wrong_answers_left": 2}}}
        exec(code, scope)
        self.assertIn("2 attempts left", scope["result"]["data"]["what_to_do_next"])

    def test_004_rpc_second_wrong_attempt_tracks_last_chance(self):
        code = make_post_process_code("verify_identity")
        scope = {"result": {"data": {"verified": False, "wrong_answers_left": 1}}}
        exec(code, scope)
        self.assertIn("1 attempts left", scope["result"]["data"]["what_to_do_next"])

    def test_005_rpc_third_wrong_attempt_triggers_terminal_closure(self):
        code = make_post_process_code("verify_identity")
        scope = {"result": {"data": {"verified": False, "wrong_answers_left": 0}}}
        exec(code, scope)
        self.assertIn("Three wrong answers reached", scope["result"]["data"]["what_to_do_next"])
        self.assertIn("close_call(outcome=\"not_verified\", reason=\"failed\")", scope["result"]["data"]["what_to_do_next"])

    def test_006_rpc_declined_identity_rules_enforced(self):
        self.assertIn("not_verified", self.all_text_a)
        self.assertIn("declined", self.all_text_a)

    def test_007_rpc_third_party_spouse_callback_protocol(self):
        self.assertIn("someone else answers", self.all_text_a)
        self.assertIn("schedule_callback", self.all_text_a)
        self.assertIn("not_reached", self.all_text_a)

    def test_008_rpc_third_party_coworker_no_disclosure(self):
        self.assertIn("NEVER reveal debt or account facts", self.all_text_a)

    def test_009_rpc_wrong_number_disposition(self):
        self.assertIn("wrong_number", self.all_text_a)

    def test_010_rpc_deceased_customer_empathy_disposition(self):
        self.assertIn("deceased", self.all_text_a)
        self.assertIn("I am sorry for your loss", self.all_text_a)

    # =========================================================================
    # Category 2: Early Arrears (1-7 Days Late) & Single Product (011 - 020)
    # =========================================================================

    def test_011_early_arrears_full_payment_today(self):
        self.assertIn("pay the full amount today", self.all_text_a)

    def test_012_early_arrears_tomorrow_option(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2026-10-14T10:00"}}
        exec(code, scope)
        self.assertIn("2026-10-15 Thursday | business day AFTER today #1", scope["vars"]["calendar_facts"])

    def test_013_early_arrears_attempt_1_this_friday(self):
        self.assertIn("Early band (days_late: 1 to 7): 1 persuasion attempt maximum", self.all_text_a)
        self.assertIn("last business day of this week (this Friday)", self.all_text_a)

    def test_014_early_arrears_single_persuasion_limit(self):
        self.assertIn("If refused, stop for this product", self.all_text_a)

    def test_015_early_arrears_readback_before_promise(self):
        self.assertIn("read back the product, amount, and date", self.all_text_a)
        self.assertIn("Do you confirm?", self.all_text_a)

    def test_016_early_arrears_mandatory_sms_utterance(self):
        self.assertIn("You will receive a text message confirming this promise", self.all_text_a)

    def test_017_early_arrears_farewell_before_close(self):
        self.assertIn("say goodbye BEFORE", self.all_text_a)

    def test_018_early_arrears_no_unsolicited_questions(self):
        self.assertIn("NEVER ask 'How much can you pay?'", self.all_text_a)

    def test_019_early_arrears_order_preservation(self):
        self.assertIn("preserve the bank's product order", self.all_text_a)

    def test_020_early_arrears_refusal_recording(self):
        self.assertIn("no_promise", self.all_text_a)
        self.assertIn("refused", self.all_text_a)

    # =========================================================================
    # Category 3: Mid & Late Arrears (8-45 Days Late) & Floor Offers (021 - 030)
    # =========================================================================

    def test_021_late_band_mandatory_two_attempts(self):
        self.assertIn("Late band (days_late: 8 to 45): EXACTLY 2 persuasion attempts required", self.all_text_a)

    def test_022_late_band_attempt_1_friday_offer(self):
        self.assertIn("Attempt 1: propose the last business day of this week (this Friday)", self.all_text_a)

    def test_023_late_band_attempt_2_floor_amount_on_deadline(self):
        self.assertIn("Attempt 2 (MANDATORY if Attempt 1 refused): propose the FLOOR amount on the product's DEADLINE date", self.all_text_a)

    def test_024_late_band_credit_card_floor_is_minimum_payment(self):
        self.assertIn("minimum_payment for credit card", self.all_text_a)

    def test_025_late_band_loan_floor_is_instalment_amount(self):
        self.assertIn("instalment_amount for loans", self.all_text_a)

    def test_026_late_band_stop_after_two_refusals(self):
        self.assertIn("Only after Attempt 2 is refused may you stop and record refusal", self.all_text_a)

    def test_027_late_band_never_repeat_refused_offer(self):
        self.assertIn("Do not repeat an offer the customer already refused", self.all_text_a)

    def test_028_late_band_overdue_remainder_explanation(self):
        self.assertIn("stating the rest stays overdue", self.all_text_a)

    def test_029_late_band_floor_calculation_in_offer_code(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-23",
            "get_account_response.data.products.0.product_id": "p_late",
            "get_account_response.data.products.0.days_late": 25,
        }}
        exec(code, scope)
        self.assertIn("DEADLINE=2026-10-23", scope["vars"]["payment_date_facts"])

    def test_030_late_band_agent_proposes_every_amount(self):
        self.assertIn("The agent proposes every amount: full past-due first, then floor", self.all_text_a)

    # =========================================================================
    # Category 4: Calendar Arithmetic, Weekend Shifts & Holidays (031 - 040)
    # =========================================================================

    def test_031_calendar_saturday_shifted_to_monday(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-17",  # Saturday
            "get_account_response.data.products.0.product_id": "p1",
            "get_account_response.data.products.0.days_late": 3,
        }}
        exec(code, scope)
        self.assertIn("NEXT VALID BUSINESS DATE ON OR AFTER OFFER: 2026-10-19 Monday", scope["vars"]["payment_date_facts"])

    def test_032_calendar_sunday_shifted_to_monday(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-18",  # Sunday
            "get_account_response.data.products.0.product_id": "p1",
            "get_account_response.data.products.0.days_late": 3,
        }}
        exec(code, scope)
        self.assertIn("NEXT VALID BUSINESS DATE ON OR AFTER OFFER: 2026-10-19 Monday", scope["vars"]["payment_date_facts"])

    def test_033_calendar_bank_holiday_shifted_to_next_business_day(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-26",  # Bank holiday Monday
            "get_account_response.data.products.0.product_id": "p1",
            "get_account_response.data.products.0.days_late": 3,
        }}
        exec(code, scope)
        self.assertIn("NEXT VALID BUSINESS DATE ON OR AFTER OFFER: 2026-10-27 Tuesday", scope["vars"]["payment_date_facts"])

    def test_034_calendar_next_friday_calculation(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2026-10-14T10:00"}}
        exec(code, scope)
        self.assertIn("2026-10-23 Friday", scope["vars"]["calendar_facts"])

    def test_035_calendar_skips_counting_today(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2026-10-14T10:00"}}
        exec(code, scope)
        self.assertIn("CALL TODAY: 2026-10-14 Wednesday", scope["vars"]["calendar_facts"])
        self.assertIn("2026-10-15 Thursday | business day AFTER today #1", scope["vars"]["calendar_facts"])

    def test_036_calendar_90_day_horizon(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2026-10-14T10:00"}}
        exec(code, scope)
        self.assertIn("business day AFTER today #40", scope["vars"]["calendar_facts"])

    def test_037_calendar_leap_year_handling(self):
        spec = calendar_spec([("brief", "Business days are Monday to Friday, except bank holidays: 2028-12-25.")])
        code = calendar_code(spec)
        scope = {"vars": {"now": "2028-02-27T10:00"}}
        exec(code, scope)
        self.assertIn("2028-02-29 Tuesday | business day AFTER today #2", scope["vars"]["calendar_facts"])

    def test_038_calendar_arbitrary_now_anchor_independence(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2027-05-05T09:00"}}
        exec(code, scope)
        self.assertIn("CALL TODAY: 2027-05-05 Wednesday", scope["vars"]["calendar_facts"])

    def test_039_calendar_holiday_in_guidance(self):
        self.assertIn("Freya Bank Holidays to skip: 2026-10-26", self.all_text_a)

    def test_040_calendar_vague_period_clarification(self):
        self.assertIn("When the customer clarifies a vague period with an exact day, use that exact day", self.all_text_a)

    # =========================================================================
    # Category 5: Boundary Limits & Deadline Enforcements (041 - 050)
    # =========================================================================

    def test_041_deadline_late_band_is_7_business_days(self):
        self.assertIn("Late Band Deadline (7 business days after today)", self.all_text_a)

    def test_042_deadline_early_band_is_12_business_days(self):
        self.assertIn("Early Band Deadline (12 business days after today, skipping 2026-10-26)", self.all_text_a)

    def test_043_deadline_after_deadline_anchoring(self):
        self.assertIn("The latest date I can record is [deadline date].", self.all_text_a)

    def test_044_deadline_outside_window_flag_in_offer(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-11-20",  # Far past deadline
            "get_account_response.data.products.0.product_id": "p_late",
            "get_account_response.data.products.0.days_late": 25,
        }}
        exec(code, scope)
        self.assertIn("outside the allowed window", scope["vars"]["payment_date_facts"])

    def test_045_deadline_within_window_preserves_offer(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-21",  # Within window
            "get_account_response.data.products.0.product_id": "p_late",
            "get_account_response.data.products.0.days_late": 25,
        }}
        exec(code, scope)
        self.assertIn("DATE TO OFFER FOR THIS PRODUCT: 2026-10-21 Wednesday", scope["vars"]["payment_date_facts"])

    def test_046_deadline_non_business_adjusted_before_deadline_comparison(self):
        self.assertIn("A holiday/weekend before the deadline is NOT a request beyond the deadline", self.all_text_a)

    def test_047_deadline_never_invent_custom_deadlines(self):
        self.assertIn("Do not invent terms, policy, tools, services, facts or outcomes", self.all_text_a)

    def test_048_deadline_independent_per_product(self):
        self.assertIn("if other products have later deadlines, keep their dates", self.all_text_a)

    def test_049_deadline_explicit_lookup_rule(self):
        self.assertIn("For an Nth-business-day deadline select the line marked #N", self.all_text_a)

    def test_050_deadline_customer_persuasion_refusal_on_deadline(self):
        self.assertIn("propose the FLOOR amount on the DEADLINE date", self.all_text_a)

    # =========================================================================
    # Category 6: Vulnerability, Hardship & Support Protocols (051 - 060)
    # =========================================================================

    def test_051_hardship_bereavement_support(self):
        self.assertIn("bereavement", self.all_text_a)
        self.assertIn("offer customer support once without persuasion", self.all_text_a)

    def test_052_hardship_illness_support(self):
        self.assertIn("illness", self.all_text_a)

    def test_053_hardship_job_loss_support(self):
        self.assertIn("job loss", self.all_text_a)

    def test_054_hardship_restructuring_transfer(self):
        self.assertIn("transfer_to_agent(queue='restructuring')", self.all_text_a)

    def test_055_hardship_note_recorded_for_multi_product(self):
        self.assertIn("add_note", self.all_text_b)
        self.assertIn("hardship", self.all_text_b)

    def test_056_hardship_transfer_suppresses_notes(self):
        self.assertIn("On any transfer (restructuring, support, general), do NOT call add_note", self.all_text_b)

    def test_057_hardship_transferred_outcome_disposition(self):
        code = make_post_process_code("transfer_to_agent")
        scope = {"result": {"data": {"ok": True}}}
        exec(code, scope)
        self.assertIn("close_call with outcome=\"transferred\"", scope["result"]["data"]["what_to_do_next"])

    def test_058_hardship_single_offer_no_badgering(self):
        self.assertIn("without persuasion", self.all_text_a)

    def test_059_hardship_customer_support_closure_reason(self):
        code = make_post_process_code("transfer_to_agent")
        scope = {"result": {"data": {"ok": True}}}
        exec(code, scope)
        self.assertIn("restructuring, human, or support", scope["result"]["data"]["what_to_do_next"])

    def test_060_hardship_tools_available_in_collection(self):
        tools = {t["function"]["name"] for t in self.wf_a["nodes"]["collection"]["tools"]}
        self.assertIn("transfer_to_agent", tools)

    # =========================================================================
    # Category 7: Debt Disputes, Fraud & Already-Paid Verifications (061 - 070)
    # =========================================================================

    def test_061_dispute_closure_outcome(self):
        self.assertIn("close as no_promise / dispute without taking a promise", self.all_text_a)

    def test_062_already_paid_one_business_day_explanation(self):
        self.assertIn("payments take one business day to appear", self.all_text_a)
        self.assertIn("close as paid", self.all_text_a)

    def test_063_already_paid_takes_no_promise(self):
        self.assertIn("take no promise, close as paid", self.all_text_a)

    def test_064_dispute_multi_product_note_reason(self):
        self.assertIn("dispute", self.all_text_b)

    def test_065_already_paid_multi_product_note_reason(self):
        self.assertIn("paid", self.all_text_b)

    def test_066_dispute_suppresses_promise_call(self):
        self.assertIn("without taking a promise", self.all_text_a)

    def test_067_dispute_tool_trigger_guarantee(self):
        tool = next(t for t in self.wf_a["nodes"]["collection"]["tools"] if t["function"]["name"] == "create_promise")
        self.assertIn("CALL only after the brief's amount/date checks", tool["function"]["description"])

    def test_068_dispute_distinguishes_questions_from_disputes(self):
        self.assertIn("Questions, digressions and incidental dates are not consent", self.all_text_a)

    def test_069_dispute_never_claims_success_without_result(self):
        tool = next(t for t in self.wf_a["nodes"]["collection"]["tools"] if t["function"]["name"] == "create_promise")
        self.assertIn("Do not claim success before the result", tool["function"]["description"])

    def test_070_dispute_outcome_enum_compliance(self):
        close_tool = next(t for t in self.wf_a["nodes"]["collection"]["tools"] if t["function"]["name"] == "close_call")
        enums = close_tool["function"]["parameters"]["properties"]["body"]["properties"]["outcome"]["enum"]
        self.assertIn("no_promise", enums)
        self.assertIn("paid", enums)

    # =========================================================================
    # Category 8: Escalations & Human Agent Demands (071 - 080)
    # =========================================================================

    def test_071_human_request_ask_once_if_can_help(self):
        self.assertIn("If human requested, ask once if you can help", self.all_text_a)

    def test_072_human_request_insist_transfers_to_human(self):
        self.assertIn("if they insist, call transfer_to_agent(queue='general')", self.all_text_a)
        self.assertIn("close as transferred / human", self.all_text_a)

    def test_073_transfer_hook_validates_ok_field(self):
        code = make_post_process_code("transfer_to_agent")
        fail_scope = {"result": {"data": {"ok": False}}}
        exec(code, fail_scope)
        self.assertNotIn("what_to_do_next", fail_scope["result"]["data"])

    def test_074_transfer_queue_enum_validity(self):
        transfer_tool = next(t for t in self.wf_a["nodes"]["collection"]["tools"] if t["function"]["name"] == "transfer_to_agent")
        queues = transfer_tool["function"]["parameters"]["properties"]["body"]["properties"]["queue"]["enum"]
        for expected in ("restructuring", "general", "support"):
            self.assertIn(expected, queues)

    def test_075_supervisor_escalation_handled_via_human_queue(self):
        self.assertIn("transferred", self.all_text_a)

    def test_076_escalation_speech_before_farewell(self):
        self.assertIn("say goodbye before", self.all_text_a.lower())

    def test_077_digital_assistant_identity_truthfulness(self):
        self.assertIn("You are the bank's digital phone assistant", self.all_text_a)

    def test_078_escalation_close_call_is_last_tool(self):
        self.assertIn("close_call is the last bank tool call", self.all_text_a)

    def test_079_escalation_no_bank_call_after_close(self):
        self.assertIn("NEVER make another bank call after close_call succeeds", self.all_text_a)

    def test_080_escalation_not_reached_callback_hook(self):
        code = make_post_process_code("schedule_callback")
        scope = {"result": {"data": {"ok": True}}}
        exec(code, scope)
        self.assertIn("close_call(outcome=\"not_reached\", reason=\"callback\")", scope["result"]["data"]["what_to_do_next"])

    # =========================================================================
    # Category 9: Multi-Product Cascades (Brief B) (081 - 090)
    # =========================================================================

    def test_081_multi_product_all_products_stated_first(self):
        self.assertIn("state each product and amount first", self.all_text_b)

    def test_082_multi_product_ask_full_payment_all_today(self):
        self.assertIn("Ask if they can pay all today", self.all_text_b)

    def test_083_multi_product_negotiate_one_by_one(self):
        self.assertIn("negotiate one-by-one in get_account order", self.all_text_b)

    def test_084_multi_product_single_combined_readback(self):
        self.assertIn("Read back all promises together for one confirmation", self.all_text_b)

    def test_085_multi_product_create_promise_called_for_each(self):
        self.assertIn("then call create_promise for each", self.all_text_b)

    def test_086_multi_product_add_note_for_every_unpromised_product(self):
        self.assertIn("call add_note(customer_id, product_id, reason)", self.all_text_b)

    def test_087_multi_product_add_note_allowed_reasons(self):
        self.assertIn("reason in ['refused', 'hardship', 'dispute', 'paid', 'service_error']", self.all_text_b)

    def test_088_multi_product_offer_code_multi_product_iteration(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-21",
            "get_account_response.data.products.0.product_id": "card_01",
            "get_account_response.data.products.0.days_late": 3,
            "get_account_response.data.products.1.product_id": "loan_02",
            "get_account_response.data.products.1.days_late": 15,
            "get_account_response.data.products.2.product_id": "overdraft_03",
            "get_account_response.data.products.2.days_late": 35,
        }}
        exec(code, scope)
        facts = scope["vars"]["payment_date_facts"]
        self.assertIn("PRODUCT card_01", facts)
        self.assertIn("PRODUCT loan_02", facts)
        self.assertIn("PRODUCT overdraft_03", facts)

    def test_089_multi_product_hook_continues_after_first_promise(self):
        code = make_post_process_code("create_promise")
        scope = {"result": {"data": {"ok": True}}}
        exec(code, scope)
        self.assertIn("If other products remain, continue negotiating or recording notes for them", scope["result"]["data"]["what_to_do_next"])

    def test_090_multi_product_terminal_close_after_all_handled(self):
        code = make_post_process_code("create_promise")
        scope = {"result": {"data": {"ok": True}}}
        exec(code, scope)
        self.assertIn("Once all products are handled, say thank you and goodbye and call close_call(outcome=\"promise\")", scope["result"]["data"]["what_to_do_next"])

    # =========================================================================
    # Category 10: Speech Disfluencies, Fault Protocols & Robustness (091 - 100)
    # =========================================================================

    def test_091_speech_correction_reconfirmation(self):
        self.assertIn("latest correction", self.all_text_a)

    def test_092_speech_partial_answer_preservation(self):
        self.assertIn("Preserve partial answers until complete", self.all_text_a)

    def test_093_speech_numbers_in_words_conversion(self):
        tool = next(t for t in self.wf_a["nodes"]["identity"]["tools"] if t["function"]["name"] == "verify_identity")
        desc = tool["function"]["parameters"]["properties"]["body"]["properties"]["answer"]["description"]
        self.assertIn("Callers say dates in words, the agent converts", desc)

    def test_094_speech_talkative_and_digression_handling(self):
        self.assertIn("Questions, digressions and incidental dates are not consent", self.all_text_a)

    def test_095_speech_one_question_at_a_time(self):
        self.assertIn("Speak English, one question at a time", self.all_text_a)

    def test_096_fault_protocol_promise_retry_once_immediately(self):
        self.assertIn("Immediately retry calling create_promise once with the exact same parameters", self.all_text_a)

    def test_097_fault_protocol_never_claim_recorded_if_failed(self):
        self.assertIn("If create_promise returns an error or ok: false, NEVER say the promise is recorded!", self.all_text_a)

    def test_098_fault_protocol_two_promise_failures_close_as_service_error(self):
        self.assertIn("close as no_promise / service_error", self.all_text_a)

    def test_099_fault_protocol_verify_identity_is_not_service_error(self):
        self.assertNotIn("Never close as service_error during identity verification", self.all_text_a)
        self.assertIn("A rejected identity answer is not a service error", self.all_text_a)

    def test_100_final_farewell_and_terminal_guarantee(self):
        self.assertIn("ALWAYS say thank you and say goodbye BEFORE", self.all_text_a)
        self.assertIn("finished", self.wf_a["nodes"])
        self.assertEqual(self.wf_a["nodes"]["finished"]["node_type"], "end_call")


if __name__ == "__main__":
    unittest.main()
