"""Tests for sorts.py. Run with:  python3 test_sorts.py   (or)   python3 -m pytest -v

sorted() is used only here, as the reference answer.
"""

import math
import random
import unittest

import sorts
from sorts import quicksort_basic, quicksort_improved

SORTS = (quicksort_basic, quicksort_improved)


class TestAgainstSorted(unittest.TestCase):
    def check(self, sort, data):
        expected = sorted(data)
        work = list(data)
        result = sort(work)
        self.assertIsNone(result)  # sorts in place, like list.sort()
        self.assertEqual(work, expected)

    def test_random_lists(self):
        # 600 lists per sort; small value ranges create many duplicates.
        rng = random.Random(303)
        for _ in range(600):
            n = rng.randint(0, 200)
            high = rng.choice([5, 100, 10**6])
            data = [rng.randint(-high, high) for _ in range(n)]
            for sort in SORTS:
                self.check(sort, data)

    def test_every_cutoff_from_the_brief(self):
        rng = random.Random(16)
        for cutoff in (1, 4, 8, 16, 32, 64):
            for _ in range(100):
                data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 150))]
                work = list(data)
                quicksort_improved(work, cutoff)
                self.assertEqual(work, sorted(data))


class TestEdgeCases(unittest.TestCase):
    def check_all(self, data):
        for sort in SORTS:
            work = list(data)
            sort(work)
            self.assertEqual(work, sorted(data), sort.__name__)

    def test_empty_list(self):
        self.check_all([])

    def test_one_element(self):
        self.check_all([42])

    def test_all_equal(self):
        self.check_all([500] * 300)

    def test_already_sorted(self):
        self.check_all(list(range(300)))

    def test_reverse_sorted(self):
        self.check_all(list(range(300, 0, -1)))

    def test_negative_numbers(self):
        self.check_all([-3, 7, -100, 0, -3, 25, -1, 8, -50, 0])

    def test_two_elements(self):
        self.check_all([2, 1])
        self.check_all([1, 2])


class TestRecursionDepth(unittest.TestCase):
    def test_improved_handles_large_bad_inputs(self):
        # 50,000 elements would need depth about 50,000 with naive recursion.
        n = 50_000
        rng = random.Random(1)
        for data in (list(range(n)), list(range(n, 0, -1)), [100] * n,
                     [rng.randint(0, 9) for _ in range(n)]):
            work = list(data)
            quicksort_improved(work)
            self.assertEqual(work, sorted(data))

    def test_improved_depth_is_logarithmic(self):
        # Wrap the recursive helper to record the deepest call. Recursing on the
        # smaller part means each call gets at most half the range: depth <= log2(n).
        original = sorts._quicksort_improved
        depth = max_depth = 0

        def tracked(a, lo, hi, cutoff):
            nonlocal depth, max_depth
            depth += 1
            max_depth = max(max_depth, depth)
            original(a, lo, hi, cutoff)
            depth -= 1

        sorts._quicksort_improved = tracked
        try:
            n = 50_000
            rng = random.Random(5)
            data = [rng.randint(0, 10**6) for _ in range(n)]
            quicksort_improved(data, cutoff=1)
        finally:
            sorts._quicksort_improved = original
        self.assertEqual(data, sorted(data))
        self.assertLessEqual(max_depth, math.log2(n) + 1)

    def test_basic_crashes_on_large_sorted_input(self):
        # Documents the bug being fixed: depth about n exceeds Python's recursion limit.
        with self.assertRaises(RecursionError):
            quicksort_basic(list(range(5_000)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
