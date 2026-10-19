import random
from Q1_naive import naive_mod_pow
from Q2_binary import binary_mod_pow


def compare_methods():
    """Check that naive and binary exponentiation always agree."""
    # Fixed cases, including edge cases that often break implementations
    fixed_cases = [
        (10, 25, 58),
        (5, 100, 13),
        (3, 13, 7),
        (2, 10, 1000),
        (7, 0, 13),    # zero exponent, answer should be 1
        (4, 5, 1),     # modulus of 1, answer should always be 0
    ]
    for a, b, m in fixed_cases:
        n = naive_mod_pow(a, b, m)
        r = binary_mod_pow(a, b, m)
        status = "OK" if n == r else "MISMATCH"
        print(f"{a}^{b} mod {m}: naive = {n}, binary = {r}  [{status}]")

    # Random cases cover far more combinations than we could write by hand.
    # The exponent is capped at 500 so the naive method stays quick.
    mismatches = 0
    for _ in range(1000):
        a = random.randint(0, 1000)
        b = random.randint(0, 500)
        m = random.randint(1, 1000)  # start at 1 because m = 0 is invalid
        if naive_mod_pow(a, b, m) != binary_mod_pow(a, b, m):
            mismatches += 1
            print(f"Mismatch for a={a}, b={b}, m={m}")

    print(f"Random tests: 1000 run, {mismatches} mismatches")


if __name__ == "__main__":
    compare_methods()