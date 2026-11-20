"""Part C: timing experiments for sorts.py.

Run:  python3 benchmark.py run1     (then: python3 benchmark.py run2)
Each run writes its own files, so nothing is overwritten:
  benchmark_output_<label>.txt   everything printed below
  timings_<label>.csv            Part C1 timings (blank time = crashed)
  timing_<label>.png             Part C1 graphs
"""

import csv
import math
import random
import sys
import time

from sorts import quicksort_basic, quicksort_improved

SIZES = [1000 * 2**k for k in range(7)]  # 1,000 ... 64,000
CUTOFFS = [1, 4, 8, 16, 32, 64]
LABEL = sys.argv[1] if len(sys.argv) > 1 else "run1"
OUT = open(f"benchmark_output_{LABEL}.txt", "w")


def report(line=""):
    print(line)
    OUT.write(line + "\n")
    OUT.flush()


def make_input(kind, n, seed):
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randint(1, 1_000_000) for _ in range(n)]
    if kind == "sorted":
        return sorted(rng.randint(1, 1_000_000) for _ in range(n))
    return [rng.randint(0, 9) for _ in range(n)]  # "duplicates": values 0 to 9


def best_time(sort, data, repeats, **kwargs):
    """Best of a few runs; each run sorts a fresh copy. Returns None on RecursionError."""
    best = math.inf
    for _ in range(repeats):
        work = list(data)
        start = time.perf_counter()
        try:
            sort(work, **kwargs)
        except RecursionError:
            return None
        best = min(best, time.perf_counter() - start)
        assert work == sorted(data), "wrong answer"  # sorted() used only to check
    return best


def part_c1():
    report("Part C1: time in seconds, best of 3 runs (CRASH = RecursionError)")
    kinds = ["random", "sorted", "duplicates"]
    header = f"{'n':>7}" + "".join(f"{k + ' basic':>18}{k + ' improved':>21}" for k in kinds)
    report(header)
    rows = []
    for n in SIZES:
        line, row = f"{n:>7}", [n]
        for kind in kinds:
            data = make_input(kind, n, seed=n)
            for sort in (quicksort_basic, quicksort_improved):
                t = best_time(sort, data, 3)
                row.append(t)
                width = 18 if sort is quicksort_basic else 21
                line += f"{('CRASH' if t is None else f'{t:.4f}'):>{width}}"
        report(line)
        rows.append(row)
    with open(f"timings_{LABEL}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n"] + [f"{k}_{s}" for k in kinds for s in ("basic", "improved")])
        writer.writerows([[r[0]] + ["" if t is None else t for t in r[1:]] for r in rows])
    return rows


def part_c3(n=100_000, rounds=5):
    """Cutoff experiment. Rounds are interleaved so slow drift affects every cutoff equally."""
    report(f"\nPart C3: quicksort_improved on {n:,} random values, best of {rounds} rounds")
    data = make_input("random", n, seed=2026)
    best = {c: math.inf for c in CUTOFFS}
    for _ in range(rounds):
        for c in CUTOFFS:
            best[c] = min(best[c], best_time(quicksort_improved, data, 1, cutoff=c))
    for c in CUTOFFS:
        report(f"  cutoff {c:>2}: {best[c]:.4f} s")
    chosen = min(best, key=best.get)
    report(f"  best cutoff: {chosen}")
    return chosen


class Counted:
    """Wraps a number and counts every comparison made on it."""
    count = 0
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        Counted.count += 1
        return self.v < other.v

    def __gt__(self, other):
        Counted.count += 1
        return self.v > other.v


def part_c4(cutoff, n=100_000):
    report(f"\nPart C4: best version (cutoff {cutoff}) against sorted(), n = {n:,}, best of 5")
    report(f"{'input':>11}{'improved (s)':>14}{'sorted() (s)':>14}{'ratio':>8}")
    for kind in ("random", "sorted", "duplicates"):
        data = make_input(kind, n, seed=7)
        mine = best_time(quicksort_improved, data, 5, cutoff=cutoff)
        start_best = math.inf
        for _ in range(5):
            work = list(data)
            start = time.perf_counter()
            sorted(work)
            start_best = min(start_best, time.perf_counter() - start)
        report(f"{kind:>11}{mine:>14.4f}{start_best:>14.4f}{mine / start_best:>7.0f}x")

    # Comparisons made: separates the algorithm's work from the language's speed.
    report("\nComparisons counted on the same input (algorithm cost, independent of language):")
    report(f"{'input':>11}{'improved':>14}{'sorted()':>14}{'n log2 n':>12}")
    for kind in ("random", "sorted", "duplicates"):
        data = [Counted(v) for v in make_input(kind, n, seed=7)]
        Counted.count = 0
        quicksort_improved(list(data), cutoff)
        mine = Counted.count
        Counted.count = 0
        sorted(data)
        report(f"{kind:>11}{mine:>14,}{Counted.count:>14,}{round(n * math.log2(n)):>12,}")


def plot(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.8), dpi=200, sharey=True)
    styles = (("basic", "#c0392b", "o"), ("improved", "#2471a3", "s"))
    for k, (ax, title) in enumerate(zip(axes, ["Random", "Already sorted", "Many duplicates (0-9)"])):
        for offset, (name, colour, marker) in enumerate(styles):
            col = 1 + 2 * k + offset
            pts = [(r[0], r[col]) for r in rows if r[col] is not None]
            if pts:
                ax.loglog(*zip(*pts), marker=marker, color=colour, markersize=4)
            crashed = [r[0] for r in rows if r[col] is None]
            if crashed:  # mark the first crash just above the bottom edge of the panel
                ax.plot(crashed[0], 0.05, "x", color=colour, markersize=8, mew=2,
                        transform=ax.get_xaxis_transform())
                ax.text(crashed[0], 0.11, f"crash from {crashed[0] // 1000}k", color=colour,
                        fontsize=7, transform=ax.get_xaxis_transform(),
                        ha="left" if crashed[0] < 8000 else "center")
        ax.set_title(title, fontsize=9)
        ax.set_xscale("log")
        ax.set_xticks(SIZES)
        ax.set_xticklabels([f"{n // 1000}k" for n in SIZES], fontsize=7)
        ax.minorticks_off()
        ax.tick_params(axis="y", labelsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel("n (log scale)", fontsize=8)
    axes[0].set_ylabel("time in seconds (log scale)", fontsize=8)
    handles = [plt.Line2D([], [], color=c, marker=m, markersize=4, label=f"quicksort_{n}")
               for n, c, m in styles]
    handles.append(plt.Line2D([], [], color="grey", marker="x", linestyle="", markersize=7,
                              mew=2, label="RecursionError (crash)"))
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=7, frameon=False)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(f"timing_{LABEL}.png")


if __name__ == "__main__":
    report(f"Benchmark {LABEL}, Python {sys.version.split()[0]}, "
           f"recursion limit {sys.getrecursionlimit()}")
    timing_rows = part_c1()
    plot(timing_rows)
    best_cutoff = part_c3()
    part_c4(best_cutoff)
    OUT.close()
