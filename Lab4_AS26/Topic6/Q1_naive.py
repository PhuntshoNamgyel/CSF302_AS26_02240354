def naive_mod_pow(a, b, m):
    """Calculate (a ** b) % m by repeated multiplication."""
    # Start from 1 because it is the identity for multiplication,
    # so the loop below builds a^b one factor at a time.
    result = 1

    for _ in range(b):
        # Taking the mod after every multiplication keeps result below m.
        # Without this, a^b would grow huge for large exponents.
        result = (result * a) % m

    # The final % m matters when b = 0 and m = 1, because 1 % 1 is 0
    return result % m


if __name__ == "__main__":
    print(naive_mod_pow(10, 25, 58))  # 56