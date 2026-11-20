"""CSF302 Assignment 2: closest pair of camera traps.

Both functions take a list of n >= 2 points (x, y) and return (d, i, j):
the smallest distance d and the indices i < j of the two points.
Distances are compared as squared values, so integer inputs are compared exactly.
"""

import math


def squared_dist(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def _check_input(points):
    if len(points) < 2:
        raise ValueError("need at least two points")


def closest_pair_brute(points):
    """Compare every pair of points: Theta(n^2)."""
    _check_input(points)
    n = len(points)
    best_d2, best_i, best_j = math.inf, -1, -1
    for i in range(n - 1):
        p = points[i]
        for j in range(i + 1, n):
            d2 = squared_dist(p, points[j])
            if d2 < best_d2:
                best_d2, best_i, best_j = d2, i, j
    return math.sqrt(best_d2), best_i, best_j


def _brute_on_indices(points, idx):
    """Base case: brute force over a small list of point indices."""
    best = (math.inf, -1, -1)
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            d2 = squared_dist(points[idx[a]], points[idx[b]])
            if d2 < best[0]:
                best = (d2, idx[a], idx[b])
    return best


def _merge_by_y(points, left, right):
    """Merge two index lists that are already sorted by y (as in merge sort)."""
    merged, a, b = [], 0, 0
    while a < len(left) and b < len(right):
        if points[left[a]][1] <= points[right[b]][1]:
            merged.append(left[a])
            a += 1
        else:
            merged.append(right[b])
            b += 1
    merged.extend(left[a:])
    merged.extend(right[b:])
    return merged


def _closest_rec(points, px):
    """px holds point indices sorted by x.

    Returns (best squared distance, i, j, the same indices sorted by y).
    """
    n = len(px)
    if n <= 3:
        d2, i, j = _brute_on_indices(points, px)
        return d2, i, j, sorted(px, key=lambda k: points[k][1])

    # Divide: split at the middle of the x-sorted order.
    mid = n // 2
    mid_x = points[px[mid]][0]

    # Conquer: solve both halves recursively.
    left = _closest_rec(points, px[:mid])
    right = _closest_rec(points, px[mid:])
    best_d2, best_i, best_j = min(left[:3], right[:3])

    # Combine: merging keeps the y-order in Theta(n) instead of re-sorting.
    py = _merge_by_y(points, left[3], right[3])

    # Strip of width 2d around the dividing line, still in y-order.
    strip = [k for k in py if (points[k][0] - mid_x) ** 2 < best_d2]

    # Packing lemma: only the next 7 strip points can be closer than d.
    for a in range(len(strip)):
        p = points[strip[a]]
        for b in range(a + 1, min(a + 8, len(strip))):
            q = points[strip[b]]
            if (q[1] - p[1]) ** 2 >= best_d2:
                break  # every later point is even further away in y
            d2 = squared_dist(p, q)
            if d2 < best_d2:
                best_d2, best_i, best_j = d2, strip[a], strip[b]

    return best_d2, best_i, best_j, py


def closest_pair(points):
    """Divide and conquer: T(n) = 2T(n/2) + Theta(n) = Theta(n log n)."""
    _check_input(points)
    px = sorted(range(len(points)), key=lambda k: points[k])  # sort once by x
    best_d2, i, j, _ = _closest_rec(points, px)
    return math.sqrt(best_d2), min(i, j), max(i, j)


if __name__ == "__main__":
    traps = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print(closest_pair_brute(traps))  # (1.414..., 0, 5)
    print(closest_pair(traps))        # (1.414..., 0, 5)
