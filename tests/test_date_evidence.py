"""Reject guessed dates from vague customer periods before computing offers."""
import unittest
from builder.calendar import offer_code, offer_extraction


class DateEvidenceTests(unittest.TestCase):
    def values(self, quote):
        return {'now': '2031-04-02T10:00', 'payment_offer_date': '2031-04-04',
                'payment_offer_quote': quote, 'payment_offer_action': 'resolve',
                'get_account_response.data.products.0.product_id': 'synthetic',
                'get_account_response.data.products.0.days_late': 2}

    def run_code(self, values):
        exec(offer_code({'holidays': ['2031-05-01']}, [[1, 20, 4]]), {'vars': values})

    def test_vague_period_with_hallucinated_iso_date_cannot_produce_offer(self):
        for quote in ('week after next', 'next week', 'later this month', 'this weekend',
                      'I can pay 540 next week', 'yes', '', 'in two weeks'):
            with self.subTest(quote=quote):
                values = self.values(quote)
                self.run_code(values)
                self.assertIn('unavailable', values['payment_date_facts'])
                self.assertNotIn('DATE TO OFFER', values['payment_date_facts'])
                self.assertEqual(values['payment_offer_action'], 'none')

    def test_explicit_days_can_reach_calendar_calculation(self):
        for quote in ('on Friday', 'the 4th', 'April 4', '4 April', '2031-04-04', 'the fourth', '4'):
            with self.subTest(quote=quote):
                values = self.values(quote)
                self.run_code(values)
                self.assertIn('DATE TO OFFER FOR THIS PRODUCT: 2031-04-04', values['payment_date_facts'])

    def test_date_evidence_cannot_be_reused_without_new_extraction(self):
        values = self.values('on Friday')
        self.run_code(values)
        self.assertEqual(values['payment_offer_quote'], '')
        self.run_code(values)
        self.assertIn('unavailable', values['payment_date_facts'])

    def test_all_extraction_fields_use_real_input_placeholders(self):
        fields = offer_extraction()
        self.assertEqual({f['name'] for f in fields}, {'payment_offer_date', 'payment_offer_quote', 'payment_offer_action'})
        for field in fields:
            for placeholder in ('{{extractor.speech}}', '{{extractor.conversation.last-10}}',
                                '{{extractor.type_preamble}}', '{{extractor.variables_list}}'):
                self.assertIn(placeholder, field['extraction_prompt'])
