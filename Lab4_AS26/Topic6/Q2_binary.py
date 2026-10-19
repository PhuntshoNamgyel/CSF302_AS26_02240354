def binary_mod_pow(a, b, m):
    """Calculate (a ** b) % m using square-and-multiply."""
    result = 1

    # Reduce the base first so every product below stays small
    a = a % m

    while b > 0:
        # If the current bit of b is 1, this power of a is part of the answer
        if b % 2 == 1:
            result = (result * a) % m

        # Square the base so it becomes a^2, a^4, a^8, ... for the next bits
        a = (a * a) % m

        # Drop the bit we just used and move to the next one
        b = b // 2

    return result % m


if __name__ == "__main__":
    print(binary_mod_pow(10, 25, 58))  # 56