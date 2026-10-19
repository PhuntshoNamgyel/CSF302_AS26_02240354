def binary_mod_pow_bitwise(a, b, m):
    """Square-and-multiply using bitwise operations on the exponent."""
    result = 1
    a = a % m

    while b > 0:
        # b & 1 isolates the lowest bit. It is 1 only when b is odd,
        # which is the same check as b % 2 == 1.
        if b & 1:
            result = (result * a) % m

        a = (a * a) % m

        # Shifting right by one bit drops the lowest bit, which is
        # the same as integer division by 2 but a bit faster.
        b >>= 1

    return result % m


if __name__ == "__main__":
    print(binary_mod_pow_bitwise(10, 25, 58))  # 56