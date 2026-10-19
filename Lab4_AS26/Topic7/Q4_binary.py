from Q1_matmul import mat_mult
from Q2_identity import identity_matrix


def matrix_pow_binary(A, n, m):
    """Calculate A^n mod m using repeated squaring."""
    if n < 0:
        raise ValueError("exponent must be non-negative")
    if m <= 0:
        raise ValueError("modulus must be a positive integer")

    result = identity_matrix(len(A))

    # Work on a reduced copy of A so the caller's matrix is never changed
    base = [[x % m for x in row] for row in A]

    while n > 0:
        # If the current bit of n is 1, multiply this power of A into the result
        if n & 1:
            result = mat_mult(result, base, m)

        # Square the base to get A^2, A^4, A^8, ... for the next bits
        base = mat_mult(base, base, m)

        # Drop the bit we just used
        n >>= 1

    return [[x % m for x in row] for row in result]


if __name__ == "__main__":
    fib = [[1, 1], [1, 0]]
    print(matrix_pow_binary(fib, 10, 1000))  # [[89, 55], [55, 34]]