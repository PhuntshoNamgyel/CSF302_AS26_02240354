def mat_mult(A, B, m):
    """Multiply two n x n matrices and reduce every entry modulo m."""
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            # Entry (i, j) is the dot product of row i of A and column j of B
            total = 0
            for k in range(n):
                total += A[i][k] * B[k][j]

            # Reduce once per entry so values stay below m instead of
            # growing larger with every repeated multiplication
            C[i][j] = total % m

    return C


if __name__ == "__main__":
    A = [[1, 1], [1, 0]]
    print(mat_mult(A, A, 100))  # [[2, 1], [1, 1]]