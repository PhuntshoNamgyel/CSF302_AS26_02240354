
import random


# 1. Bottom-up dynamic programming
def matrix_chain_dp(p):
    n = len(p) - 1
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float("inf")

            for k in range(i, j):
                value = (
                    cost[i][k]
                    + cost[k + 1][j]
                    + p[i] * p[k + 1] * p[j + 1]
                )

                if value < cost[i][j]:
                    cost[i][j] = value
                    split[i][j] = k

    # 2. Reconstruct optimal parenthesisation
    def parenthesize(i, j):
        if i == j:
            return f"A{i + 1}"

        k = split[i][j]
        return f"({parenthesize(i, k)}{parenthesize(k + 1, j)})"

    return cost[0][n - 1], parenthesize(0, n - 1)


# 3. Brute-force recursive verification
def brute_force(p, i, j):
    if i == j:
        return 0

    return min(
        brute_force(p, i, k)
        + brute_force(p, k + 1, j)
        + p[i] * p[k + 1] * p[j + 1]
        for k in range(i, j)
    )


# 4. Left-to-right multiplication cost
def left_to_right(p):
    return sum(
        p[0] * p[i] * p[i + 1]
        for i in range(1, len(p) - 1)
    )


# 5. Given test cases
chains = [
    ("Given 1", [30, 35, 15, 5, 10, 20, 25]),
    ("Given 2", [5, 4, 6, 2, 7])
]

# Generate 5 random chains with up to 8 matrices
random.seed(42)

for i in range(1, 6):
    n = random.randint(3, 8)
    dimensions = [random.randint(2, 30) for _ in range(n + 1)]
    chains.append((f"Random {i}", dimensions))


# 6. Display and verify results
for name, p in chains:
    optimal_cost, order = matrix_chain_dp(p)
    brute_cost = brute_force(p, 0, len(p) - 2)
    left_cost = left_to_right(p)

    print(f"\n{name}: {p}")
    print(f"Optimal Cost: {optimal_cost}")
    print(f"Left-to-Right Cost: {left_cost}")
    print(f"Optimal Parenthesisation: {order}")
    print(f"Brute-Force Verification: {'PASS' if optimal_cost == brute_cost else 'FAIL'}")
