import time
from Q1_naive import naive_mod_pow
from Q2_binary import binary_mod_pow


def time_methods():
    """Time both methods as the exponent grows by a factor of 10 each row."""
    a, m = 7, 1000003
    exponents = [10, 100, 1000, 10000, 100000, 1000000]
    print(f"{'exponent':>10} | {'naive (s)':>12} | {'binary (s)':>12}")

    for b in exponents:
        # perf_counter is the right clock for timing short pieces of code
        start = time.perf_counter()
        naive_mod_pow(a, b, m)
        naive_time = time.perf_counter() - start

        # One binary call finishes in microseconds, which is too small to
        # measure reliably. Running it many times and averaging fixes that.
        runs = 1000
        start = time.perf_counter()
        for _ in range(runs):
            binary_mod_pow(a, b, m)
        binary_time = (time.perf_counter() - start) / runs

        print(f"{b:>10} | {naive_time:>12.6f} | {binary_time:>12.8f}")

    # Expected pattern: naive time grows with b (about b multiplications),
    # while binary barely changes (about log2(b) multiplications).


if __name__ == "__main__":
    time_methods()