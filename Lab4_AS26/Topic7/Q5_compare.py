import random
from Q3_naive import matrix_pow_naive
from Q4_binary import matrix_pow_binary


def random_matrix(size, max_value):
    """Build a size x size matrix with random entries from 0 to max_value."""
    return [[random.randint(0, max_value) for _ in range(size)]
            for _ in range(size)]


def compare_methods():
    """Check that naive and binary matrix exponentiation always agree."""
    fixed_cases = [
        ([[1, 1], [1, 0]], 10, 1000),
        ([[2, 3], [4, 5]], 7, 97),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 5, 1000),
        ([[3, 1], [2, 4]], 0, 50),    # zero exponent gives the identity
        ([[3, 1], [2, 4]], 6, 1),     # modulus of 1 gives all zeros
    ]
    for A, n, m in fixed_cases:
        naive = matrix_pow_naive(A, n, m)
        binary = matrix_pow_binary(A, n, m)
        status = "OK" if naive == binary else "MISMATCH"
        print(f"A={A}, n={n}, m={m}: {status}")

    # Random matrices of different sizes cover far more combinations.
    # The exponent is capped at 50 so the naive method stays quick.
    mismatches = 0
    for _ in range(500):
        size = random.randint(2, 4)
        A = random_matrix(size, 9)
        n = random.randint(0, 50)
        m = random.randint(1, 1000)
        if matrix_pow_naive(A, n, m) != matrix_pow_binary(A, n, m):
            mismatches += 1
            print(f"Mismatch for A={A}, n={n}, m={m}")

    print(f"Random tests: 500 run, {mismatches} mismatches")


if __name__ == "__main__":
    compare_methods()