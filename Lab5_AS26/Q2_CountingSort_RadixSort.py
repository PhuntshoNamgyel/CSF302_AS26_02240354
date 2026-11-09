
import random
import time
from array import array
from pathlib import Path

import matplotlib.pyplot as plt


def counting_sort(items, k, key=lambda x: x):
    # Count how many times each key from 0 to k appears.
    # Use a compact integer array to save memory for large k.
    count = array('I', [0]) * (k + 1)

    for item in items:
        count[key(item)] += 1

    # Convert frequencies into cumulative counts.
    # Each count now gives the ending position of that key.
    for i in range(1, k + 1):
        count[i] += count[i - 1]

    result = [None] * len(items)

    # Process backwards to preserve the order of equal keys.
    # This makes counting sort stable.
    for item in reversed(items):
        value = key(item)
        count[value] -= 1
        result[count[value]] = item

    return result


def radix_sort(items, base):
    # LSD radix sort processes digits from right to left.
    # Each digit is sorted using stable counting sort.
    result = list(items)

    if not result:
        return result

    largest = max(result)
    place = 1

    # Continue until all digits have been processed.
    while largest // place > 0:
        # Extract the current digit and sort by that digit.
        result = counting_sort(
            result, base - 1, key=lambda x: (x // place) % base
        )

        # Move to the next digit (10 or 256 positions).
        place *= base

    return result


# Original merge sort from Lab 1.
def MergeSort_354(data_354):
    if len(data_354) <= 1:
        return data_354

    mid_354 = len(data_354) // 2
    left_354 = MergeSort_354(data_354[:mid_354])
    right_354 = MergeSort_354(data_354[mid_354:])

    return Merge_354(left_354, right_354)


def Merge_354(left_354, right_354):
    result_354 = []
    i_354 = 0
    j_354 = 0

    while i_354 < len(left_354) and j_354 < len(right_354):
        if left_354[i_354] <= right_354[j_354]:
            result_354.append(left_354[i_354])
            i_354 += 1
        else:
            result_354.append(right_354[j_354])
            j_354 += 1

    result_354.extend(left_354[i_354:])
    result_354.extend(right_354[j_354:])

    return result_354


def measure(sort_function, data, expected):
    # Measure only the sorting time, excluding data generation.
    start = time.perf_counter()
    result = sort_function(data)
    elapsed_ms = (time.perf_counter() - start) * 1000

    # Check that the algorithm sorted the data correctly.
    assert result == expected, "Incorrect sorting result"

    return elapsed_ms


def demonstrate_stability():
    # Each pair contains (key, original index).
    # Sort by key while keeping equal keys in their original order.
    pairs = [(3, 0), (1, 1), (3, 2),
             (2, 3), (1, 4), (3, 5)]

    result = counting_sort(pairs, 3, key=lambda pair: pair[0])

    # Verify that sorting is both correct and stable.
    assert result == sorted(pairs, key=lambda pair: pair[0])

    print("STABILITY TEST (key, original index)")
    print("Before:", pairs)
    print("After: ", result)
    print("Equal keys keep their original order.\n")


def benchmark_counting(rng):
    # Keep n fixed at 100,000 while increasing the key range k.
    n = 100_000
    k_values = [10, 1_000, 100_000, 10_000_000]

    counting_times = []
    merge_times = []

    print("COUNTING SORT VS MERGE SORT (n = 100,000)")
    print(f'{"k":>12} {"Counting (ms)":>16} {"Merge (ms)":>14}')

    for k in k_values:
        # Generate the same data for both algorithms.
        data = [rng.randint(0, k) for _ in range(n)]
        expected = sorted(data)

        counting_ms = measure(
            lambda a: counting_sort(a, k), data, expected
        )
        merge_ms = measure(MergeSort_354, data, expected)

        counting_times.append(counting_ms)
        merge_times.append(merge_ms)

        print(f"{k:>12,} {counting_ms:>16.3f} {merge_ms:>14.3f}")

    # Plot execution time against the maximum key k.
    plt.figure(figsize=(8, 5))
    plt.plot(k_values, counting_times, 'o-', label='Counting sort')
    plt.plot(k_values, merge_times, 's-', label='Lab 1 merge sort')
    plt.xscale('log')

    plt.xlabel('Maximum key k (log scale)')
    plt.ylabel('Execution time (ms)')
    plt.title('Counting sort vs merge sort (n = 100,000)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        Path(__file__).with_name('q2_counting_plot.png'), dpi=160
    )
    plt.close()
    print()


def benchmark_radix(rng):
    # Keep k fixed at 10^9 while increasing the input size n.
    k = 10**9
    sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000]

    base10_times = []
    base256_times = []
    merge_times = []

    print("RADIX SORT VS MERGE SORT (k = 10^9)")
    print(
        f'{"n":>12} {"Base 10 (ms)":>16} '
        f'{"Base 256 (ms)":>16} {"Merge (ms)":>14}'
    )

    for n in sizes:
        # All three algorithms use the same input data.
        data = [rng.randint(0, k) for _ in range(n)]
        expected = sorted(data)

        base10_ms = measure(
            lambda a: radix_sort(a, 10), data, expected
        )
        base256_ms = measure(
            lambda a: radix_sort(a, 256), data, expected
        )
        merge_ms = measure(MergeSort_354, data, expected)

        base10_times.append(base10_ms)
        base256_times.append(base256_ms)
        merge_times.append(merge_ms)

        print(
            f"{n:>12,} {base10_ms:>16.3f} "
            f"{base256_ms:>16.3f} {merge_ms:>14.3f}"
        )

    # Plot execution time against the input size n.
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, base10_times, 'o-', label='Radix sort (base 10)')
    plt.plot(sizes, base256_times, 's-', label='Radix sort (base 256)')
    plt.plot(sizes, merge_times, '^-', label='Lab 1 merge sort')

    plt.xlabel('Input size n')
    plt.ylabel('Execution time (ms)')
    plt.title('Radix sort vs merge sort (k = 10^9)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        Path(__file__).with_name('q2_radix_plot.png'), dpi=160
    )
    plt.close()


if __name__ == "__main__":
    rng = random.Random(42)

    demonstrate_stability()
    benchmark_counting(rng)
    benchmark_radix(rng)

    print("\nPlots saved: q2_counting_plot.png and q2_radix_plot.png")
