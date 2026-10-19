from Q4_binary import matrix_pow_binary


def fib_mod(n, m):
    """Return the nth Fibonacci number modulo m using matrix exponentiation."""
    # The Fibonacci matrix raised to the nth power is
    #   [[F(n+1), F(n)  ],
    #    [F(n),   F(n-1)]]
    # so F(n) can be read straight from the top right entry.
    fib_matrix = [[1, 1], [1, 0]]
    result = matrix_pow_binary(fib_matrix, n, m)
    return result[0][1]


if __name__ == "__main__":
    # F(0) to F(10) are 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55
    print([fib_mod(i, 1000) for i in range(11)])
    print(fib_mod(10, 7))      # 55 % 7 = 6
    print(fib_mod(50, 10**9))  # F(50) = 12586269025, so this is 586269025