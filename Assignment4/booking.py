"""CSF302 Assignment 4: booking the hall.

Each request is (start, finish, fee) with start < finish. Two requests fit together
if one finishes no later than the other starts, so 9-12 and 12-14 both fit.
Every function returns (total_fee, chosen), where chosen is a sorted list of indices.
"""

from bisect import bisect_right
from itertools import combinations


def fits(a, b):
    """True if requests a and b can both use the hall."""
    return a[1] <= b[0] or b[1] <= a[0]


def greedy_earliest_finish(requests):
    """Sort by finish time and accept each request that starts after the last accepted one ends."""
    chosen, last_finish = [], float("-inf")
    for i in sorted(range(len(requests)), key=lambda i: requests[i][1]):
        start, finish, _ = requests[i]
        if start >= last_finish:
            chosen.append(i)
            last_finish = finish
    return sum(requests[i][2] for i in chosen), sorted(chosen)


def greedy_highest_fee(requests):
    """Sort by fee, highest first, and accept each request that fits with all accepted ones."""
    chosen = []
    for i in sorted(range(len(requests)), key=lambda i: -requests[i][2]):
        if all(fits(requests[i], requests[j]) for j in chosen):
            chosen.append(i)
    return sum(requests[i][2] for i in chosen), sorted(chosen)


def best_schedule(requests):
    """Weighted interval scheduling by dynamic programming.

    With requests sorted by finish time (positions 1..n):
      OPT(j) = best total fee using only the first j requests
      OPT(0) = 0
      OPT(j) = max(OPT(j - 1), fee_j + OPT(p(j)))
    where p(j) = number of earlier requests that finish at or before request j starts.
    """
    order = sorted(range(len(requests)), key=lambda i: requests[i][1])
    finishes = [requests[i][1] for i in order]
    n = len(order)

    opt = [0] * (n + 1)
    p = [0] * (n + 1)
    for j in range(1, n + 1):
        start, _, fee = requests[order[j - 1]]
        p[j] = bisect_right(finishes, start, 0, j - 1)  # binary search: O(log n)
        opt[j] = max(opt[j - 1], fee + opt[p[j]])

    # Reconstruction: walk back through the table and repeat each winning choice.
    chosen, j = [], n
    while j > 0:
        fee = requests[order[j - 1]][2]
        if fee + opt[p[j]] > opt[j - 1]:  # taking request j was better
            chosen.append(order[j - 1])
            j = p[j]
        else:                             # skipping request j was at least as good
            j -= 1
    return opt[n], sorted(chosen)


def brute_force(requests):
    """Try every subset (for checking only). Exponential: Theta(2^n * n^2)."""
    n = len(requests)
    if n > 15:
        raise ValueError("brute force is only for n <= 15")
    best_total, best_set = 0, []
    for size in range(1, n + 1):
        for subset in combinations(range(n), size):
            if all(fits(requests[a], requests[b]) for a, b in combinations(subset, 2)):
                total = sum(requests[i][2] for i in subset)
                if total > best_total:
                    best_total, best_set = total, list(subset)
    return best_total, best_set


if __name__ == "__main__":
    requests = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]
    for func in (greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force):
        print(f"{func.__name__:>22}: {func(requests)}")
