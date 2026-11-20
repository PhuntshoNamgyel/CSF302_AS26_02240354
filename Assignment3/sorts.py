"""CSF302 Assignment 3: fixing a slow quicksort.

Both functions sort a list of integers in place into ascending order.
"""

import random


def lomuto_partition(a, lo, hi):
    """Partition a[lo..hi] around the pivot a[hi]; return the pivot's final index."""
    pivot = a[hi]
    i = lo - 1  # a[lo..i] holds elements <= pivot
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def _quicksort_basic(a, lo, hi):
    if lo < hi:
        p = lomuto_partition(a, lo, hi)
        _quicksort_basic(a, lo, p - 1)
        _quicksort_basic(a, p + 1, hi)


def quicksort_basic(a):
    """Textbook quicksort: Lomuto partition with the last element as pivot.

    Sorted input or many equal keys give splits of n - 1 and 0, so
    T(n) = T(n - 1) + Theta(n) = Theta(n^2) and the recursion depth is about n.
    """
    _quicksort_basic(a, 0, len(a) - 1)


def insertion_sort_range(a, lo, hi):
    """Insertion sort on a[lo..hi]; fast for small ranges."""
    for i in range(lo + 1, hi + 1):
        key = a[i]
        j = i - 1
        while j >= lo and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def partition_3way(a, lo, hi):
    """Dutch national flag partition around the pivot a[lo].

    Returns (lt, gt) with a[lo..lt-1] < pivot, a[lt..gt] == pivot, a[gt+1..hi] > pivot.
    """
    pivot = a[lo]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1  # do not advance i: the swapped-in a[i] is unexamined
        else:
            i += 1
    return lt, gt


def _quicksort_improved(a, lo, hi, cutoff):
    while hi - lo + 1 > cutoff:
        # Random pivot: no fixed input (such as sorted data) is a bad case.
        k = random.randint(lo, hi)
        a[lo], a[k] = a[k], a[lo]
        lt, gt = partition_3way(a, lo, hi)  # keys equal to the pivot are finished

        # Recurse on the smaller part and loop on the larger one: depth O(log n).
        if lt - lo < hi - gt:
            _quicksort_improved(a, lo, lt - 1, cutoff)
            lo = gt + 1
        else:
            _quicksort_improved(a, gt + 1, hi, cutoff)
            hi = lt - 1
    insertion_sort_range(a, lo, hi)  # small part left over


def quicksort_improved(a, cutoff=16):
    """Random pivot, 3-way partition, insertion sort for parts of size <= cutoff,
    and recursion on the smaller part only."""
    _quicksort_improved(a, 0, len(a) - 1, cutoff)


if __name__ == "__main__":
    amounts = [500, 100, 2500, 100, 500, 50, 1000, 100]
    for sort in (quicksort_basic, quicksort_improved):
        data = list(amounts)
        sort(data)
        print(f"{sort.__name__}: {data}")
