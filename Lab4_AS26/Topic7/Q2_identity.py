def identity_matrix(n):
    """Return the n x n identity matrix (1s on the diagonal, 0s elsewhere)."""
    # The identity plays the same role for matrices that 1 plays for numbers:
    # multiplying any matrix by it leaves the matrix unchanged.
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


if __name__ == "__main__":
    for row in identity_matrix(3):
        print(row)