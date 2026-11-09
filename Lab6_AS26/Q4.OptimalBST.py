
# Given probabilities
p = [0, 0.15, 0.10, 0.05, 0.10, 0.20]
q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]


# 1. Compute optimal BST using bottom-up DP
def optimal_bst(p, q):
    n = len(p) - 1

    cost = [[0.0] * (n + 1) for _ in range(n + 2)]
    weight = [[0.0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 2)]

    for i in range(1, n + 2):
        cost[i][i - 1] = q[i - 1]
        weight[i][i - 1] = q[i - 1]

    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1

            cost[i][j] = float("inf")
            weight[i][j] = weight[i][j - 1] + p[j] + q[j]

            for r in range(i, j + 1):
                value = (
                    cost[i][r - 1]
                    + cost[r + 1][j]
                    + weight[i][j]
                )

                if value < cost[i][j]:
                    cost[i][j] = value
                    root[i][j] = r

    return cost[1][n], root


# 2. Print the optimal tree structure
def print_tree(root, i, j, level=0, position="Root"):
    indent = "    " * level

    if i > j:
        print(f"{indent}{position}: d{i - 1}")
        return

    r = root[i][j]
    print(f"{indent}{position}: k{r}")

    print_tree(root, i, r - 1, level + 1, "Left")
    print_tree(root, r + 1, j, level + 1, "Right")


# 3. Display results
min_cost, root = optimal_bst(p, q)

print(f"Minimum Expected Search Cost: {min_cost:.2f}")
print("\nOptimal BST Structure:")
print_tree(root, 1, len(p) - 1)
