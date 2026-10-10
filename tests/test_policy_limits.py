"""Attempt budgets must come from the supplied policy, not public-case heuristics."""
import unittest
from builder.core import persuasion_limits


class PolicyLimitsTests(unittest.TestCase):
    def test_attempt_count_is_independent_of_deadline_length(self):
        policy='| days_late | Band | Deadline | Persuasion attempts |\n| --- | --- | --- | --- |\n| 2 to 9 | custom | the 1st business day after today | 4 |\n| 10 to 60 | other | the 20th business day after today | 0 |'
        self.assertEqual(persuasion_limits([('policy',policy)]),[[2,9,4],[10,60,0]])

    def test_missing_or_ambiguous_limit_is_not_guessed(self):
        for policy in ('| days_late | Deadline |\n| 1 to 9 | 4 days |',
                       '| days_late | Persuasion attempts |\n| 1 to 9 | maybe two |',
                       '| days_late | Persuasion attempts |\n| 1 to 9 | 1 |\n| 8 to 20 | 2 |'):
            with self.subTest(policy=policy): self.assertIsNone(persuasion_limits([('policy',policy)]))


if __name__ == '__main__': unittest.main()
