
import random
from time import perf_counter


# 1. Randomized quickselect (k-th smallest element)
def quickselect(arr, k, rng):
    left, right = 0, len(arr) - 1
    k -= 1

    while left <= right:
        pivot = arr[rng.randint(left, right)]
        low, current, high = left, left, right

        while current <= high:
            if arr[current] < pivot:
                arr[low], arr[current] = arr[current], arr[low]
                low += 1
                current += 1
            elif arr[current] > pivot:
                arr[current], arr[high] = arr[high], arr[current]
                high -= 1
            else:
                current += 1

        if k < low:
            right = low - 1
        elif k > high:
            left = high + 1
        else:
            return arr[k]


# 2. Trial division up to square root of n
def trial_division(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    divisor = 5

    while divisor * divisor <= n:
        if n % divisor == 0 or n % (divisor + 2) == 0:
            return False
        divisor += 6

    return True


# Miller-Rabin probabilistic primality test
def miller_rabin(n, rounds, rng):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = rng.randint(2, n - 2)
        x = pow(a, d, n)

        if x in (1, n - 1):
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return False

    return True


# 1. Compare quickselect with sorting and indexing
rng = random.Random(42)
pivot_rng = random.Random(123)

print("Randomized Quickselect vs Sorting")
print(
    f"{'n':>10} {'k':>10} {'Quickselect (ms)':>18} "
    f"{'Sorting (ms)':>15} {'Match':>8}"
)

for n in [10_000, 100_000, 1_000_000]:
    arr = [rng.randrange(10_000_000) for _ in range(n)]
    k = (n + 1) // 2

    start = perf_counter()
    selected = quickselect(arr.copy(), k, pivot_rng)
    quick_time = (perf_counter() - start) * 1000

    start = perf_counter()
    sorted_value = sorted(arr)[k - 1]
    sort_time = (perf_counter() - start) * 1000

    match = selected == sorted_value
    assert match

    print(
        f"{n:>10} {k:>10} {quick_time:>18.4f} "
        f"{sort_time:>15.4f} {str(match):>8}"
    )


# 2. Compare Miller-Rabin with trial division
rng = random.Random(42)
mr_rng = random.Random(123)

print("\nMiller-Rabin vs Trial Division (20 Random 12-Digit Numbers)")
print(
    f"{'Number':>13} {'Trial (ms)':>12} "
    f"{'MR (ms)':>12} {'Trial':>10} {'MR':>10} {'Agree':>8}"
)

matches = 0

for _ in range(20):
    n = rng.randint(100_000_000_000, 999_999_999_999)

    start = perf_counter()
    trial_result = trial_division(n)
    trial_time = (perf_counter() - start) * 1000

    start = perf_counter()
    mr_result = miller_rabin(n, 10, mr_rng)
    mr_time = (perf_counter() - start) * 1000

    agree = trial_result == mr_result
    matches += agree

    print(
        f"{n:>13} {trial_time:>12.4f} "
        f"{mr_time:>12.4f} {str(trial_result):>10} "
        f"{str(mr_result):>10} {str(agree):>8}"
    )

print(f"\nAgreement: {matches}/20")
assert matches == 20


# 3. Test Carmichael number 561 with one round
rng = random.Random(456)
trials = 1000
prime_count = 0

for _ in range(trials):
    if miller_rabin(561, 1, rng):
        prime_count += 1

print("\nMiller-Rabin on Carmichael Number 561")
print("Number: 561")
print("Rounds per test: 1")
print("Total Tests:", trials)
print("Answered Prime:", prime_count)
print("Answered Composite:", trials - prime_count)
print(f"False Positive Rate: {prime_count / trials * 100:.2f}%")
