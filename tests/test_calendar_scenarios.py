"""Offline calendar and schema checks; these do not simulate conversations."""
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


class CalendarAndSchemaTests(unittest.TestCase):
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

    def test_012_early_arrears_tomorrow_option(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2026-10-14T10:00"}}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("2026-10-15 Thursday | business day AFTER today #1", scope["vars"]["calendar_facts"])

    def test_029_late_band_floor_calculation_in_offer_code(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-23",
            "get_account_response.data.products.0.product_id": "p_late",
            "get_account_response.data.products.0.days_late": 25,
        }}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("DEADLINE=2026-10-23", scope["vars"]["payment_date_facts"])

    def test_031_calendar_saturday_shifted_to_monday(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-17",  # Saturday
            "get_account_response.data.products.0.product_id": "p1",
            "get_account_response.data.products.0.days_late": 3,
        }}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("NEXT VALID BUSINESS DATE ON OR AFTER OFFER: 2026-10-19 Monday", scope["vars"]["payment_date_facts"])

    def test_032_calendar_sunday_shifted_to_monday(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-18",  # Sunday
            "get_account_response.data.products.0.product_id": "p1",
            "get_account_response.data.products.0.days_late": 3,
        }}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("NEXT VALID BUSINESS DATE ON OR AFTER OFFER: 2026-10-19 Monday", scope["vars"]["payment_date_facts"])

    def test_033_calendar_bank_holiday_shifted_to_next_business_day(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-26",  # Bank holiday Monday
            "get_account_response.data.products.0.product_id": "p1",
            "get_account_response.data.products.0.days_late": 3,
        }}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("NEXT VALID BUSINESS DATE ON OR AFTER OFFER: 2026-10-27 Tuesday", scope["vars"]["payment_date_facts"])

    def test_034_calendar_next_friday_calculation(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2026-10-14T10:00"}}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("2026-10-23 Friday", scope["vars"]["calendar_facts"])

    def test_035_calendar_skips_counting_today(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2026-10-14T10:00"}}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("CALL TODAY: 2026-10-14 Wednesday", scope["vars"]["calendar_facts"])
        self.assertIn("2026-10-15 Thursday | business day AFTER today #1", scope["vars"]["calendar_facts"])

    def test_036_calendar_90_day_horizon(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2026-10-14T10:00"}}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("business day AFTER today #40", scope["vars"]["calendar_facts"])

    def test_037_calendar_leap_year_handling(self):
        spec = calendar_spec([("brief", "Business days are Monday to Friday, except bank holidays: 2028-12-25.")])
        code = calendar_code(spec)
        scope = {"vars": {"now": "2028-02-27T10:00"}}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("2028-02-29 Tuesday | business day AFTER today #2", scope["vars"]["calendar_facts"])

    def test_038_calendar_arbitrary_now_anchor_independence(self):
        code = calendar_code(self.cal_spec)
        scope = {"vars": {"now": "2027-05-05T09:00"}}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("CALL TODAY: 2027-05-05 Wednesday", scope["vars"]["calendar_facts"])

    def test_044_deadline_outside_window_flag_in_offer(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-11-20",  # Far past deadline
            "get_account_response.data.products.0.product_id": "p_late",
            "get_account_response.data.products.0.days_late": 25,
        }}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("outside the allowed window", scope["vars"]["payment_date_facts"])

    def test_045_deadline_within_window_preserves_offer(self):
        code = offer_code(self.cal_spec, self.bands)
        scope = {"vars": {
            "now": "2026-10-14T10:00", "payment_offer_date": "2026-10-21",  # Within window
            "get_account_response.data.products.0.product_id": "p_late",
            "get_account_response.data.products.0.days_late": 25,
        }}
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        self.assertIn("DATE TO OFFER FOR THIS PRODUCT: 2026-10-21 Wednesday", scope["vars"]["payment_date_facts"])

    def test_060_hardship_tools_available_in_collection(self):
        tools = {t["function"]["name"] for t in self.wf_a["nodes"]["collection"]["tools"]}
        self.assertIn("transfer_to_agent", tools)

    def test_070_dispute_outcome_enum_compliance(self):
        close_tool = next(t for t in self.wf_a["nodes"]["collection"]["tools"] if t["function"]["name"] == "close_call")
        enums = close_tool["function"]["parameters"]["properties"]["body"]["properties"]["outcome"]["enum"]
        self.assertIn("no_promise", enums)
        self.assertIn("paid", enums)

    def test_074_transfer_queue_enum_validity(self):
        transfer_tool = next(t for t in self.wf_a["nodes"]["collection"]["tools"] if t["function"]["name"] == "transfer_to_agent")
        queues = transfer_tool["function"]["parameters"]["properties"]["body"]["properties"]["queue"]["enum"]
        for expected in ("restructuring", "general", "support"):
            self.assertIn(expected, queues)

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
        scope["vars"]["payment_offer_quote"] = str(scope["vars"].get("payment_offer_date", ""))
        exec(code, scope)
        facts = scope["vars"]["payment_date_facts"]
        self.assertIn("PRODUCT card_01", facts)
        self.assertIn("PRODUCT loan_02", facts)
        self.assertIn("PRODUCT overdraft_03", facts)
