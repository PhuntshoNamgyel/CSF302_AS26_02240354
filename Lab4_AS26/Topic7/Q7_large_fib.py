from Q6_fibonacci import fib_mod

MOD = 10**9 + 7  # a common large prime modulus


if __name__ == "__main__":
    # Each call below needs only about log2(n) matrix multiplications.
    # A loop that builds every earlier Fibonacci number would need n steps,
    # which is impossible for n = 10^18.
    for n in [100, 1000, 10**6, 10**9, 10**18]:
        print(f"F({n}) mod {MOD} = {fib_mod(n, MOD)}")