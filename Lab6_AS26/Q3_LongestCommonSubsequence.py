
import random
from time import perf_counter


# 1. Bottom-up LCS table
def lcs_table(x, y):
    dp = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp


# 2. Reconstruct one LCS
def reconstruct_lcs(x, y, dp):
    i, j = len(x), len(y)
    result = []

    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            result.append(x[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(result))


# 3. Space-optimised LCS using two rows
def lcs_two_rows(x, y):
    previous = [0] * (len(y) + 1)

    for a in x:
        current = [0] * (len(y) + 1)

        for j, b in enumerate(y, 1):
            if a == b:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])

        previous = current

    return previous[-1]


# 4. Brute-force solution using subsequences
def brute_force(x, y):
    best = 0

    for mask in range(1 << len(x)):
        length = mask.bit_count()
        if length <= best:
            continue

        subsequence = (
            x[i] for i in range(len(x)) if mask & (1 << i)
        )
        remaining = iter(y)

        if all(char in remaining for char in subsequence):
            best = length

    return best


# 5. Line-by-line diff using LCS
def print_diff(old_lines, new_lines):
    dp = lcs_table(old_lines, new_lines)
    i, j = len(old_lines), len(new_lines)
    changes = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and old_lines[i - 1] == new_lines[j - 1]:
            changes.append("  " + old_lines[i - 1])
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            changes.append("+ " + new_lines[j - 1])
            j -= 1
        else:
            changes.append("- " + old_lines[i - 1])
            i -= 1

    for line in reversed(changes):
        print(line)


# Display LCS table and sequence
X = "ABCBDAB"
Y = "BDCABA"

dp = lcs_table(X, Y)

print("LCS Table")
print("    -  " + "  ".join(Y))

for i, row in enumerate(dp):
    label = X[i - 1] if i > 0 else "-"
    print(f"{label:>3} " + "  ".join(str(value) for value in row))

lcs = reconstruct_lcs(X, Y, dp)
print(f"\nLCS: {lcs}")
print(f"LCS Length: {dp[-1][-1]}")
print(f"Two-Row LCS Length: {lcs_two_rows(X, Y)}")


# Compare DP and brute-force running times
print("\nPerformance Comparison (milliseconds)")
print(f"{'Length':>6} {'DP Time':>12} {'Brute Time':>12}")

random.seed(42)

for n in range(5, 19):
    x = "".join(random.choices("ABCD", k=n))
    y = "".join(random.choices("ABCD", k=n))

    start = perf_counter()
    dp_length = lcs_table(x, y)[-1][-1]
    dp_time = (perf_counter() - start) * 1000

    start = perf_counter()
    brute_length = brute_force(x, y)
    brute_time = (perf_counter() - start) * 1000

    assert dp_length == brute_length == lcs_two_rows(x, y)

    print(f"{n:>6} {dp_time:>12.4f} {brute_time:>12.4f}")


# Compare two text files
with open("old.txt", encoding="utf-8") as file:
    old_lines = file.read().splitlines()

with open("new.txt", encoding="utf-8") as file:
    new_lines = file.read().splitlines()

print("\nLine-by-Line Diff")
print_diff(old_lines, new_lines)
