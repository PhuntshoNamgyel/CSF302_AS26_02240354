import random
import time
from Q3_naive import matrix_pow_naive
from Q4_binary import matrix_pow_binary


def random_matrix(size, max_value):
    """Build a size x size matrix with random entries from 0 to max_value."""
    return [[random.randint(0, max_value) for _ in range(size)]
            for _ in range(size)]


def benchmark():
    """Time both methods across matrix sizes and exponents."""
    m = 10**9 + 7
    sizes = [2, 4, 8, 16]
    exponents = [10, 100, 1000]

    print(f"{'size':>5} | {'exponent':>8} | {'naive (ms)':>11} | "
          f"{'binary (ms)':>11} | {'speedup':>8}")

    for size in sizes:
        A = random_matrix(size, 9)
        for n in exponents:
            # perf_counter is the right clock for timing short pieces of code
            start = time.perf_counter()
            matrix_pow_naive(A, n, m)
            naive_ms = (time.perf_counter() - start) * 1000

            start = time.perf_counter()
            matrix_pow_binary(A, n, m)
            binary_ms = (time.perf_counter() - start) * 1000

            speedup = naive_ms / binary_ms
            print(f"{size:>5} | {n:>8} | {naive_ms:>11.3f} | "
                  f"{binary_ms:>11.3f} | {speedup:>7.1f}x")

    # Expected pattern: naive time grows with n and roughly with size^3,
    # while binary grows only with log2(n) and size^3.


if __name__ == "__main__":
    benchmark()