"""Part C: counterexample search, greedy-to-optimal revenue ratios, and complexity checks.

Run:  python3 analysis.py run1
Writes analysis_output_<label>.txt and ratios_<label>.png. The random inputs use fixed seeds, so the counterexamples
and ratios are the same on every machine; only the timings change.
"""

import random
import sys
import time
from itertools import combinations_with_replacement

from booking import best_schedule, brute_force, greedy_earliest_finish, greedy_highest_fee

LABEL = sys.argv[1] if len(sys.argv) > 1 else "run1"
OUT = open(f"analysis_output_{LABEL}.txt", "w")
GREEDY = {"earliest finish": greedy_earliest_finish, "highest fee": greedy_highest_fee}


def report(line=""):
    print(line)
    OUT.write(line + "\n")
    OUT.flush()


def random_requests(rng, n):
    """Requests over about four days: start hour 0-100, 1-12 hours long, fee Nu 500-10,000."""
    requests = []
    for _ in range(n):
        start = rng.randint(0, 100)
        requests.append((start, start + rng.randint(1, 12), rng.randint(1, 20) * 500))
    return requests


def counterexample_search():
    """Smallest inputs where each rule loses: every multiset of 2-4 requests with
    times 0-4 and fees 1-3, checked against the DP optimum."""
    report("C1: smallest counterexamples (times 0-4, fees 1-3, sizes 2 to 4)")
    pool = [(s, f, w) for s in range(5) for f in range(s + 1, 5) for w in (1, 2, 3)]
    found = {}
    for size in (2, 3, 4):
        for combo in combinations_with_replacement(pool, size):
            requests = list(combo)
            opt = best_schedule(requests)[0]
            losers = [name for name, rule in GREEDY.items() if rule(requests)[0] < opt]
            for name in losers:
                found.setdefault(name, (size, requests, opt))
            if len(losers) == 2:
                found.setdefault("both rules", (size, requests, opt))
    for name in ("earliest finish", "highest fee", "both rules"):
        size, requests, opt = found[name]
        got = {r: GREEDY[r](requests)[0] for r in GREEDY}
        report(f"  {name:>15}: {size} requests {requests}  greedy {got}  optimum {opt}")


def ratio_experiment(trials=1000, n=50, seed=4):
    report(f"\nC3: {trials} random inputs of {n} requests (greedy revenue / optimal revenue)")
    rng = random.Random(seed)
    ratios = {name: [] for name in GREEDY}
    for _ in range(trials):
        requests = random_requests(rng, n)
        opt = best_schedule(requests)[0]
        for name, rule in GREEDY.items():
            ratios[name].append(rule(requests)[0] / opt)
    report(f"{'rule':>16}{'average':>10}{'worst':>9}{'best':>8}{'optimal in':>13}")
    for name, values in ratios.items():
        hits = sum(r == 1 for r in values)
        report(f"{name:>16}{sum(values) / trials:>10.3f}{min(values):>9.3f}{max(values):>8.3f}"
               f"{hits:>9} / {trials}")
    plot_ratios(ratios)


def plot_ratios(ratios):
    """Histogram of the greedy / optimal revenue ratios for both rules."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=200)
    bins = [0.4 + 0.025 * k for k in range(25)]
    colours = ("#c0392b", "#2471a3")
    labels = [f"{name} (average {sum(v) / len(v):.3f})" for name, v in ratios.items()]
    ax.hist(list(ratios.values()), bins=bins, color=colours, label=labels)  # bars side by side
    for values, colour in zip(ratios.values(), colours):
        ax.axvline(sum(values) / len(values), color=colour, linestyle="--", linewidth=1)
    ax.set_xlabel("greedy revenue / optimal revenue", fontsize=8)
    ax.set_ylabel("number of inputs", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc="upper left")
    fig.tight_layout()
    fig.savefig(f"ratios_{LABEL}.png")


def small_input_hit_rate(trials=1000, seed=10):
    """How often each greedy rule happens to be optimal on small inputs like the tests use."""
    report(f"\nGreedy optimal on small inputs ({trials} inputs of 0 to 10 requests):")
    rng = random.Random(seed)
    hits = {name: 0 for name in GREEDY}
    for _ in range(trials):
        requests = random_requests(rng, rng.randint(0, 10))
        opt = brute_force(requests)[0]
        for name, rule in GREEDY.items():
            hits[name] += rule(requests)[0] == opt
    for name, count in hits.items():
        report(f"  {name:>15}: optimal on {count} of {trials} ({100 * count / trials:.1f}%)")


def best_time(func, data, repeats=5):
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        func(data)
        best = min(best, time.perf_counter() - start)
    return best


def spread_requests(n, seed):
    """n requests spread over 2n hours, so the number accepted grows with n."""
    rng = random.Random(seed)
    requests = []
    for _ in range(n):
        start = rng.randint(0, 2 * n)
        requests.append((start, start + rng.randint(1, 12), rng.randint(1, 20) * 500))
    return requests


def complexity_check():
    report("\nC4: doubling check, best of 5 runs (seconds; ratio = T(2n)/T(n))")
    funcs = [greedy_earliest_finish, greedy_highest_fee, best_schedule]
    report(f"{'n':>7}" + "".join(f"{f.__name__:>24}" for f in funcs))
    previous = None
    for n in [1000 * 2**k for k in range(5)]:
        data = spread_requests(n, seed=n)
        times = [best_time(f, data) for f in funcs]
        cells = [f"{t:.4f}" + (f" (x{t / p:.2f})" if previous else "")
                 for t, p in zip(times, previous or times)]
        report(f"{n:>7}" + "".join(f"{c:>24}" for c in cells))
        previous = times

    # Worst case for brute force: no two requests overlap, so every subset is fully checked.
    report("brute_force on requests that never overlap (one extra request at a time):")
    previous = None
    for n in range(10, 16):
        t = best_time(brute_force, [(2 * i, 2 * i + 1, 500) for i in range(n)], 3)
        report(f"  n = {n}: {t:.4f} s" + (f"  (x{t / previous:.2f})" if previous else ""))
        previous = t


if __name__ == "__main__":
    report(f"Analysis {LABEL}, Python {sys.version.split()[0]}")
    counterexample_search()
    ratio_experiment()
    small_input_hit_rate()
    complexity_check()
    OUT.close()
