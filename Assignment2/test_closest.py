"""Tests for closest.py. Run with:  python -m pytest -v   (or)   python test_closest.py"""

import math
import random
import unittest

from closest import closest_pair, closest_pair_brute


def assert_valid(test, points, result, expected_d):
    """Check that result = (d, i, j) has the right distance and a real pair i < j at that distance."""
    d, i, j = result
    test.assertTrue(math.isclose(d, expected_d, abs_tol=1e-9), f"{d} != {expected_d}")
    test.assertTrue(0 <= i < j < len(points), f"bad indices {i}, {j}")
    test.assertTrue(math.isclose(math.dist(points[i], points[j]), d, abs_tol=1e-9))


class TestAgainstBruteForce(unittest.TestCase):
    def test_random_integer_inputs(self):
        # Small coordinate range so ties and duplicate points appear often.
        rng = random.Random(302)
        for _ in range(600):
            n = rng.randint(2, 50)
            points = [(rng.randint(0, 30), rng.randint(0, 30)) for _ in range(n)]
            expected = closest_pair_brute(points)
            assert_valid(self, points, closest_pair(points), expected[0])

    def test_random_float_inputs(self):
        rng = random.Random(2024)
        for _ in range(600):
            n = rng.randint(2, 50)
            points = [(rng.uniform(-100, 100), rng.uniform(-100, 100)) for _ in range(n)]
            expected = closest_pair_brute(points)
            self.assertEqual(closest_pair(points), expected)  # no ties, so indices must match too

    def test_larger_random_input(self):
        rng = random.Random(7)
        points = [(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(2000)]
        assert_valid(self, points, closest_pair(points), closest_pair_brute(points)[0])


class TestEdgeCases(unittest.TestCase):
    def test_example_from_brief(self):
        points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        for func in (closest_pair, closest_pair_brute):
            d, i, j = func(points)
            self.assertAlmostEqual(d, math.sqrt(2))
            self.assertEqual((i, j), (0, 5))

    def test_exactly_two_points(self):
        points = [(7, 1), (4, 5)]
        for func in (closest_pair, closest_pair_brute):
            self.assertEqual(func(points), (5.0, 0, 1))

    def test_duplicate_points_give_zero(self):
        points = [(5, 5), (1, 9), (8, 2), (1, 9), (3, 3)]
        for func in (closest_pair, closest_pair_brute):
            self.assertEqual(func(points), (0.0, 1, 3))

    def test_many_duplicates_split_across_halves(self):
        # Eight copies of one point: the copies end up in both halves of the recursion.
        points = [(4, 4)] * 8 + [(0, 0), (9, 9)]
        assert_valid(self, points, closest_pair(points), 0.0)

    def test_all_points_on_one_vertical_line(self):
        ys = [0, 9, 3, 20, 14, 7, 30, 26]  # closest y values are 7 and 9 (gap 2)
        points = [(5, y) for y in ys]
        for func in (closest_pair, closest_pair_brute):
            self.assertEqual(func(points), (2.0, 1, 5))

    def test_vertical_line_random(self):
        rng = random.Random(1)
        for _ in range(200):
            points = [(3, rng.randint(0, 200)) for _ in range(rng.randint(2, 50))]
            assert_valid(self, points, closest_pair(points), closest_pair_brute(points)[0])

    def test_closest_pair_across_dividing_line(self):
        # Sorted by x, the split is between (5, 5) and (6, 5). Each half alone has
        # a best distance of sqrt(50), but the crossing pair is only 1 apart.
        points = [(11, 10), (5, 5), (0, 0), (11, 0), (6, 5), (0, 10)]
        by_x = sorted(range(len(points)), key=lambda k: points[k])
        left_half = set(by_x[:3])
        d, i, j = closest_pair(points)
        self.assertEqual((d, i, j), (1.0, 1, 4))
        self.assertTrue((i in left_half) != (j in left_half))  # one point on each side
        self.assertEqual(closest_pair_brute(points), (1.0, 1, 4))

    def test_fewer_than_two_points_rejected(self):
        for func in (closest_pair, closest_pair_brute):
            with self.assertRaises(ValueError):
                func([(1, 1)])
            with self.assertRaises(ValueError):
                func([])


if __name__ == "__main__":
    unittest.main(verbosity=2)
