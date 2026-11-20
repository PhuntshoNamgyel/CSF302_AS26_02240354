"""Tests for booking.py. Run with:  python3 test_booking.py   (or)   python3 -m pytest -v"""

import random
import unittest
from itertools import combinations

from booking import (best_schedule, brute_force, fits, greedy_earliest_finish,
                     greedy_highest_fee)

ALL = (greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force)
EXAMPLE = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]


def random_requests(rng, n, equal_fees=False):
    requests = []
    for _ in range(n):
        start = rng.randint(0, 20)
        fee = 1000 if equal_fees else rng.randint(1, 20) * 500
        requests.append((start, start + rng.randint(1, 6), fee))
    return requests


class Helpers(unittest.TestCase):
    def assert_valid(self, requests, result):
        """chosen must be sorted unique indices, pairwise compatible, and add up to total."""
        total, chosen = result
        self.assertEqual(chosen, sorted(set(chosen)))
        self.assertTrue(all(0 <= i < len(requests) for i in chosen))
        for a, b in combinations(chosen, 2):
            self.assertTrue(fits(requests[a], requests[b]), f"{a} and {b} overlap")
        self.assertEqual(total, sum(requests[i][2] for i in chosen))


class TestAgainstBruteForce(Helpers):
    def test_dp_matches_brute_force(self):
        rng = random.Random(404)
        for _ in range(600):
            requests = random_requests(rng, rng.randint(0, 10))
            expected = brute_force(requests)[0]
            result = best_schedule(requests)
            self.assert_valid(requests, result)
            self.assertEqual(result[0], expected)

    def test_greedy_results_are_valid_and_never_beat_optimum(self):
        rng = random.Random(7)
        for _ in range(300):
            requests = random_requests(rng, rng.randint(0, 10))
            best = best_schedule(requests)[0]
            for greedy in (greedy_earliest_finish, greedy_highest_fee):
                result = greedy(requests)
                self.assert_valid(requests, result)
                self.assertLessEqual(result[0], best)

    def test_equal_fees_earliest_finish_is_optimal(self):
        rng = random.Random(1000)
        for _ in range(600):
            requests = random_requests(rng, rng.randint(0, 10), equal_fees=True)
            self.assertEqual(greedy_earliest_finish(requests)[0], brute_force(requests)[0])


class TestEdgeCases(Helpers):
    def test_example_from_brief(self):
        self.assertEqual(greedy_earliest_finish(EXAMPLE), (7500, [0, 3, 4]))
        self.assertEqual(best_schedule(EXAMPLE), (10000, [1, 4]))
        self.assertEqual(brute_force(EXAMPLE), (10000, [1, 4]))

    def test_no_requests(self):
        for func in ALL:
            self.assertEqual(func([]), (0, []))

    def test_one_request(self):
        for func in ALL:
            self.assertEqual(func([(10, 14, 5000)]), (5000, [0]))

    def test_all_overlapping(self):
        # Every request covers 12:00 to 13:00, so only one can be accepted.
        requests = [(9, 17, 6000), (10, 13, 2000), (11, 16, 9000), (12, 14, 1500)]
        self.assertEqual(best_schedule(requests), (9000, [2]))
        self.assertEqual(brute_force(requests), (9000, [2]))
        self.assertEqual(greedy_highest_fee(requests), (9000, [2]))
        self.assertEqual(greedy_earliest_finish(requests), (2000, [1]))  # ends first, at 13

    def test_none_overlapping(self):
        requests = [(15, 17, 1000), (8, 10, 3000), (11, 13, 2000)]
        for func in ALL:
            self.assertEqual(func(requests), (6000, [0, 1, 2]))

    def test_back_to_back(self):
        # An event ending at 12 and one starting at 12 both fit.
        requests = [(12, 14, 2500), (9, 12, 3000), (14, 18, 4000)]
        for func in ALL:
            self.assertEqual(func(requests), (9500, [0, 1, 2]))

    def test_brute_force_rejects_large_input(self):
        with self.assertRaises(ValueError):
            brute_force([(i, i + 1, 100) for i in range(16)])


class TestCounterexamples(unittest.TestCase):
    """The Part C counterexamples used in the report."""

    def test_earliest_finish_fails(self):
        requests = [(9, 12, 3000), (10, 16, 8000)]  # workshop, wedding
        self.assertEqual(greedy_earliest_finish(requests)[0], 3000)
        self.assertEqual(best_schedule(requests)[0], 8000)

    def test_highest_fee_fails(self):
        requests = [(9, 17, 9000), (9, 13, 5000), (13, 17, 6000)]
        self.assertEqual(greedy_highest_fee(requests)[0], 9000)
        self.assertEqual(best_schedule(requests)[0], 11000)

    def test_both_rules_fail(self):
        requests = [(9, 10, 1000), (9, 17, 9000), (9, 13, 5000), (13, 17, 6000)]
        self.assertEqual(greedy_earliest_finish(requests)[0], 7000)
        self.assertEqual(greedy_highest_fee(requests)[0], 9000)
        self.assertEqual(best_schedule(requests)[0], 11000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
