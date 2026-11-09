
from time import perf_counter

prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
prices += [3 * i for i in range(11, 26)]


# 1. Naive recursive solution
def naive(n, calls):
    calls[0] += 1
    if n == 0:
        return 0

    return max(prices[i] + naive(n - i, calls) for i in range(1, n + 1))


# 2. Top-down memoized solution
def memoized(n, calls):
    cache = [-1] * (n + 1)
    cache[0] = 0

    def solve(length):
        calls[0] += 1
        if cache[length] != -1:
            return cache[length]

        cache[length] = max(
            prices[i] + solve(length - i)
            for i in range(1, length + 1)
        )
        return cache[length]

    return solve(n)


# 3. Bottom-up tabulated solution
def bottom_up(n):
    dp = [0] * (n + 1)
    first_cut = [0] * (n + 1)

    for length in range(1, n + 1):
        for cut in range(1, length + 1):
            revenue = prices[cut] + dp[length - cut]

            if revenue > dp[length]:
                dp[length] = revenue
                first_cut[length] = cut

    pieces = []
    while n > 0:
        pieces.append(first_cut[n])
        n -= first_cut[n]

    return dp[len(dp) - 1], pieces


# 4. Maximum revenue and optimal pieces for n = 1 to 10
print("Maximum Revenue and Optimal Cuts")
print(f"{'n':>2} {'Revenue':>8}  Pieces")

for n in range(1, 11):
    revenue, pieces = bottom_up(n)
    print(f"{n:>2} {revenue:>8}  {pieces}")


# 5. Recursive call counts and execution times
print("\nBenchmark (time in milliseconds)")
print(
    f"{'n':>2} {'Naive Calls':>12} {'Naive Time':>12} "
    f"{'Memo Calls':>12} {'Memo Time':>12} "
    f"{'BU Calls':>10} {'BU Time':>10}"
)

for n in [5, 10, 15, 20, 25]:
    naive_calls = [0]
    start = perf_counter()
    result1 = naive(n, naive_calls)
    naive_time = (perf_counter() - start) * 1000

    memo_calls = [0]
    start = perf_counter()
    result2 = memoized(n, memo_calls)
    memo_time = (perf_counter() - start) * 1000

    start = perf_counter()
    result3, _ = bottom_up(n)
    bottom_time = (perf_counter() - start) * 1000

    assert result1 == result2 == result3

    print(
        f"{n:>2} {naive_calls[0]:>12,} {naive_time:>12.3f} "
        f"{memo_calls[0]:>12,} {memo_time:>12.3f} "
        f"{0:>10} {bottom_time:>10.3f}"
    )
