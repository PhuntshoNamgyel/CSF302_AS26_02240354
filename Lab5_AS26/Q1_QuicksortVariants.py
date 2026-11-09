import random
import time


def lomuto_partition(a, lo, hi):
    # Lomuto uses the last element as its pivot.
    pivot = a[hi]
    i = lo  # Where the next element <= pivot should go.

    for j in range(lo, hi):
        if a[j] <= pivot:
            if i != j:
                a[i], a[j] = a[j], a[i]
            i += 1

    # Put the pivot between the smaller and larger elements.
    a[i], a[hi] = a[hi], a[i]
    return i - 1, i + 1, hi - lo  # Left end, right start, comparisons.


def hoare_partition(a, lo, hi):
    # Choose the middle value, then move it to the first position.
    mid = (lo + hi) // 2
    a[lo], a[mid] = a[mid], a[lo]
    pivot = a[lo]
    i, j = lo - 1, hi + 1
    comparisons = 0

    while True:
        # Scan from the left until an element >= pivot is found.
        while True:
            i += 1
            comparisons += 1
            if a[i] >= pivot:
                break

        # Scan from the right until an element <= pivot is found.
        while True:
            j -= 1
            comparisons += 1
            if a[j] <= pivot:
                break

        # When the pointers cross, the two partitions are ready.
        if i >= j:
            return j, j + 1, comparisons

        # Swap the elements found on the wrong sides.
        a[i], a[j] = a[j], a[i]


def randomized_partition(a, lo, hi):
    # Pick a random pivot, then use Lomuto partitioning.
    k = random.randint(lo, hi)
    a[k], a[hi] = a[hi], a[k]
    return lomuto_partition(a, lo, hi)


def three_way_partition(a, lo, hi):
    # Keep three groups: < pivot, == pivot, and > pivot.
    pivot = a[(lo + hi) // 2]
    lt, i, gt = lo, lo, hi
    comparisons = 0

    while i <= gt:
        comparisons += 1  # Check a[i] < pivot.

        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        else:
            comparisons += 1  # Check a[i] > pivot.

            if a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1  # Recheck the element swapped into position i.
            else:
                i += 1  # Equal values are already in the middle group.

    # The equal group [lt, gt] needs no further sorting.
    return lt - 1, gt + 1, comparisons


def quicksort(a, partition):
    comparisons = 0

    def sort(lo, hi):
        nonlocal comparisons

        while lo < hi:
            # Partition returns the two ranges still needing sorting.
            left_end, right_start, count = partition(a, lo, hi)
            comparisons += count

            # Recurse on the smaller range and loop over the larger one.
            # This avoids deep recursion even with unbalanced partitions.
            if left_end - lo < hi - right_start:
                sort(lo, left_end)
                lo = right_start
            else:
                sort(right_start, hi)
                hi = left_end

    sort(0, len(a) - 1)
    return comparisons


def main():
    random.seed(42)  # Make random pivot choices repeatable.
    rng = random.Random(42)  # Generate the same test data each run.

    variants = {
        "Lomuto": lomuto_partition,
        "Hoare": hoare_partition,
        "Randomized": randomized_partition,
        "Three-way": three_way_partition
    }

    sizes = [1000, 2000, 4000, 8000, 16000]

    print(f'{"Size":>6}  {"Input":<12} {"Variant":<12} '
          f'{"Comparisons":>14} {"Time (ms)":>12}')
    print("-" * 65)

    for n in sizes:
        # Test each algorithm on four kinds of input.
        cases = {
            "Random": [rng.randrange(n * 10) for _ in range(n)],
            "Sorted": list(range(n)),
            "Reverse": list(range(n - 1, -1, -1)),
            "Duplicates": [rng.randrange(10) for _ in range(n)]
        }

        for input_type, data in cases.items():
            expected = sorted(data)

            for name, partition in variants.items():
                a = data.copy()  # Each variant receives identical input.

                start = time.perf_counter()
                comparisons = quicksort(a, partition)
                elapsed_ms = (time.perf_counter() - start) * 1000

                # Confirm that the result matches Python's sorted order.
                assert a == expected, f"Incorrect result: {name}"

                print(f"{n:>6}  {input_type:<12} {name:<12} "
                      f"{comparisons:>14,} {elapsed_ms:>12.3f}")


if __name__ == "__main__":
    main()
