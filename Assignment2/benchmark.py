"""Part C: timing experiment, crossover search and log-log graph.

Run:  python benchmark.py
Outputs: a printed timing table, the crossover point, timings.csv and loglog.png.
"""

import csv
import math
import multiprocessing as mp
import random
import time

from closest import closest_pair, closest_pair_brute

SIZES = [1000 * 2**k for k in range(7)]  # 1,000 ... 64,000
BRUTE_LIMIT = 60  # seconds; brute force is stopped after this
SEED = 302


def make_points(n, seed):
    """n random camera traps on a 1,000,000 x 1,000,000 map grid."""
    rng = random.Random(seed)
    return [(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(n)]


def best_time(func, points, repeats):
    """Best of a few runs, as in the doubling experiment from notes 2.1."""
    best = math.inf
    for _ in range(repeats):
        start = time.perf_counter()
        func(points)
        best = min(best, time.perf_counter() - start)
    return best


def _brute_worker(points, repeats, queue):
    queue.put(best_time(closest_pair_brute, points, repeats))


def time_brute_with_limit(points, repeats):
    """Run brute force in a child process so it can be stopped at the time limit."""
    queue = mp.Queue()
    worker = mp.Process(target=_brute_worker, args=(points, repeats, queue))
    worker.start()
    worker.join(BRUTE_LIMIT * repeats)
    if worker.is_alive():
        worker.terminate()
        worker.join()
        return None  # did not finish within the limit
    return queue.get()


def timing_experiment():
    rows, brute_running = [], True
    print(f"{'n':>7} {'brute (s)':>14} {'D&C (s)':>9} {'brute ratio':>12} {'D&C ratio':>10}")
    for n in SIZES:
        points = make_points(n, SEED + n)
        d_time = best_time(closest_pair, points, 3)
        if brute_running:
            b_time = time_brute_with_limit(points, 3 if n <= 4000 else 1)
            b_text = f"{b_time:.3f}" if b_time is not None else f">{BRUTE_LIMIT} stopped"
            brute_running = b_time is not None
        else:
            b_time, b_text = None, "not run"
        # Doubling ratio T(2n)/T(n) for each column (notes 2.1).
        prev = rows[-1] if rows else None
        rb = f"{b_time / prev[1]:.2f}" if prev and prev[1] and b_time else "-"
        rd = f"{d_time / prev[2]:.2f}" if prev else "-"
        print(f"{n:>7} {b_text:>14} {d_time:>9.4f} {rb:>12} {rd:>10}")
        rows.append((n, b_time, d_time))
    return rows


def find_crossover(max_n=150, inputs_per_n=40, repeats=9):
    """Smallest n where divide and conquer is faster than brute force.

    For each n, both functions solve the same 40 random inputs; the batch is timed
    9 times and the fastest batch is kept to reduce noise.
    """
    results = []
    for n in range(2, max_n + 1):
        batch = [make_points(n, SEED * 1000 + n * 50 + k) for k in range(inputs_per_n)]
        times = []
        for func in (closest_pair_brute, closest_pair):
            best = math.inf
            for _ in range(repeats):
                start = time.perf_counter()
                for pts in batch:
                    func(pts)
                best = min(best, time.perf_counter() - start)
            times.append(best / inputs_per_n)
        results.append((n, times[0], times[1]))
    # Crossover: first n after which D&C is faster for every larger n tested.
    crossover = None
    for k in range(len(results)):
        if all(b > d for _, b, d in results[k:]):
            crossover = results[k][0]
            break
    first_win = next(n for n, b, d in results if b > d)
    return results, first_win, crossover


def fit_slope(rows, col):
    """Least-squares slope of log(time) against log(n): the empirical exponent."""
    pts = [(math.log(r[0]), math.log(r[col])) for r in rows if r[col]]
    mx = sum(x for x, _ in pts) / len(pts)
    my = sum(y for _, y in pts) / len(pts)
    return sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)


def plot(rows, path="loglog.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=200)
    brute = [(n, b) for n, b, _ in rows if b]
    ax.loglog([n for n, _ in brute], [b for _, b in brute], "o-", color="#c0392b",
              label="Brute force (measured)")
    ax.loglog([r[0] for r in rows], [r[2] for r in rows], "s-", color="#2471a3",
              label="Divide and conquer (measured)")
    # Dashed reference lines anchored at the first data point of each series.
    ns = [r[0] for r in rows]
    n0, b0 = brute[0]
    ax.loglog(ns, [b0 * (n / n0) ** 2 for n in ns], "--", color="#c0392b", alpha=0.45,
              label=r"$c\,n^2$ reference")
    d0 = rows[0][2]
    ax.loglog(ns, [d0 * (n * math.log2(n)) / (ns[0] * math.log2(ns[0])) for n in ns], "--",
              color="#2471a3", alpha=0.45, label=r"$c\,n\log n$ reference")
    ax.axhline(BRUTE_LIMIT, color="grey", linestyle=":", linewidth=1)
    ax.text(ns[-1], BRUTE_LIMIT * 1.2, "60 s limit", color="grey", fontsize=8, ha="right")
    stopped = [n for n, b, _ in rows if b is None and n > brute[-1][0]][:1]
    if stopped:  # brute force was stopped here, so its time is only known to exceed 60 s
        ax.plot(stopped, [BRUTE_LIMIT], "^", color="#c0392b", markerfacecolor="white")
        ax.annotate("brute force stopped", (stopped[0], BRUTE_LIMIT), xytext=(-8, 5),
                    textcoords="offset points", ha="right", fontsize=8, color="#c0392b")
    ax.set_xlabel("Number of camera traps, n (log scale)")
    ax.set_ylabel("Running time in seconds (log scale)")
    ax.set_title("Closest pair: running time against n")
    ax.set_xticks(ns)
    ax.set_xticklabels([f"{n // 1000}k" for n in ns])
    ax.minorticks_off()
    ax.grid(True, which="major", alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(path)


if __name__ == "__main__":
    rows = timing_experiment()
    with open("timings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "brute_seconds", "dc_seconds"])
        writer.writerows(rows)
    print(f"\nEmpirical exponent (log-log slope): brute {fit_slope(rows, 1):.2f}, "
          f"D&C {fit_slope(rows, 2):.2f}")
    plot(rows)

    results, first_win, crossover = find_crossover()
    print(f"\nFirst n where D&C wins: {first_win}; faster for every n >= {crossover}")
    print(f"{'n':>4} {'brute (us)':>11} {'D&C (us)':>9}")
    for n, b, d in results:
        if n <= 10 or 15 <= n <= 45 or n % 10 == 0:
            print(f"{n:>4} {b * 1e6:>11.1f} {d * 1e6:>9.1f}")
