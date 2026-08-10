import time


def IsPrimeTrialDivision_354(n_354):
    if n_354 < 2:
        return False

    for divisor_354 in range(2, int(n_354 ** 0.5) + 1):
        if n_354 % divisor_354 == 0:
            return False

    return True


def GeneratePrimesTrialDivision_354(limit_354):
    primes_354 = []

    for num_354 in range(2, limit_354 + 1):
        if IsPrimeTrialDivision_354(num_354):
            primes_354.append(num_354)

    return primes_354


def IsPrimeOptimized_354(n_354):
    if n_354 < 2:
        return False
    if n_354 == 2:
        return True
    if n_354 % 2 == 0:
        return False

    for divisor_354 in range(3, int(n_354 ** 0.5) + 1, 2):
        if n_354 % divisor_354 == 0:
            return False

    return True


def GeneratePrimesOptimized_354(limit_354):
    primes_354 = []

    if limit_354 >= 2:
        primes_354.append(2)

    for num_354 in range(3, limit_354 + 1, 2):
        if IsPrimeOptimized_354(num_354):
            primes_354.append(num_354)

    return primes_354


def SieveOfEratosthenes_354(limit_354):
    is_prime_354 = [True] * (limit_354 + 1)
    is_prime_354[0] = False
    if limit_354 >= 1:
        is_prime_354[1] = False

    for num_354 in range(2, int(limit_354 ** 0.5) + 1):
        if is_prime_354[num_354]:
            for multiple_354 in range(num_354 * num_354, limit_354 + 1, num_354):
                is_prime_354[multiple_354] = False

    primes_354 = [num_354 for num_354 in range(2, limit_354 + 1) if is_prime_354[num_354]]

    return primes_354


def MeasureTime_354(func_354, limit_354):
    start_354 = time.perf_counter()
    primes_354 = func_354(limit_354)
    end_354 = time.perf_counter()
    return len(primes_354), end_354 - start_354


if __name__ == "__main__":
    input_sizes_354 = [10000, 50000, 100000, 500000, 1000000]

    print(f"{'N':<12}{'Naive (s)':<14}{'Optimized (s)':<16}{'Sieve (s)':<14}")
    print("-" * 56)

    for limit_354 in input_sizes_354:
        naive_count_354, naive_time_354 = MeasureTime_354(GeneratePrimesTrialDivision_354, limit_354)
        optimized_count_354, optimized_time_354 = MeasureTime_354(GeneratePrimesOptimized_354, limit_354)
        sieve_count_354, sieve_time_354 = MeasureTime_354(SieveOfEratosthenes_354, limit_354)

        print(f"{limit_354:<12}{naive_time_354:<14.6f}{optimized_time_354:<16.6f}{sieve_time_354:<14.6f}")