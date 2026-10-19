from Q4_bitwise import binary_mod_pow_bitwise


def safe_mod_pow(a, b, m):
    """Validate the inputs, then calculate (a ** b) % m."""
    # Floats and strings would give wrong results or confusing errors later
    if not all(isinstance(x, int) for x in (a, b, m)):
        raise TypeError("a, b and m must all be integers")

    # m = 0 would mean dividing by zero. Negative moduli are not supported.
    if m <= 0:
        raise ValueError("modulus must be a positive integer")

    # A negative exponent means a^(-b) = 1 / a^b, which needs a modular
    # inverse. That is a different algorithm and may not exist, so reject it.
    if b < 0:
        raise ValueError("exponent must be non-negative")

    # Anything to the power 0 is 1. The % m handles m = 1, where the answer is 0.
    if b == 0:
        return 1 % m

    # A negative base needs no special case. For a positive m, Python's %
    # always returns a value in [0, m), so reducing the base fixes it.
    return binary_mod_pow_bitwise(a, b, m)


if __name__ == "__main__":
    tests = [
        (3, 0, 7),    # zero exponent
        (3, -2, 7),   # negative exponent, should raise an error
        (-3, 5, 7),   # negative base, should still work
        (3, 5, 0),    # zero modulus, should raise an error
        (3, 5, -7),   # negative modulus, should raise an error
        (3, 5, 7),    # normal case
    ]
    for a, b, m in tests:
        try:
            print(f"safe_mod_pow({a}, {b}, {m}) = {safe_mod_pow(a, b, m)}")
        except (ValueError, TypeError) as error:
            print(f"safe_mod_pow({a}, {b}, {m}) -> error: {error}")

    # Python's built-in pow should agree with our negative base result
    print("Built-in pow(-3, 5, 7) =", pow(-3, 5, 7))