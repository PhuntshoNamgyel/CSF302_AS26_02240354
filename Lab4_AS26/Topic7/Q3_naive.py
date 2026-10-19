from Q1_matmul import mat_mult
from Q2_identity import identity_matrix


def matrix_pow_naive(A, n, m):
    """Calculate A^n mod m using n repeated matrix multiplications."""
    if n < 0:
        raise ValueError("exponent must be non-negative")
    if m <= 0:
        raise ValueError("modulus must be a positive integer")

    # Start from the identity, just like starting from 1 for numbers,
    # so A^0 correctly comes out as the identity matrix
    result = identity_matrix(len(A))

    for _ in range(n):
        result = mat_mult(result, A, m)

    # Final reduction matters when n = 0 and m = 1, because the identity
    # matrix has 1s that should become 0 under modulus 1
    return [[x % m for x in row] for row in result]


if __name__ == "__main__":
    fib = [[1, 1], [1, 0]]
    print(matrix_pow_naive(fib, 10, 1000))  # [[89, 55], [55, 34]]