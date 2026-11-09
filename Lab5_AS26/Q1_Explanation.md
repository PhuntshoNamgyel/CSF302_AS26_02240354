# Q1: Quicksort Variants — Explanation

## 1. How each variant works

- **Lomuto:** Uses the **last element** as the pivot. Moves values less than or equal to the pivot to the left, then places the pivot in its final position. Sorted and reverse-sorted inputs cause highly uneven partitions.
- **Hoare:** Uses the **middle element as the pivot value**. Two pointers scan from opposite ends and swap misplaced values. When they cross, the array is divided into two ranges.
- **Randomised:** Chooses a **random pivot**, moves it to the end, then applies Lomuto partitioning. Random pivots help avoid consistently poor splits on ordered inputs.
- **Three-way (Dutch national flag):** Divides elements into **less than**, **equal to**, and **greater than** the pivot. The equal group is already in place and is not sorted again.

## 2. Important parts of the code

- `lo` and `hi` are the start and end indices of the current range.
- Each partition function returns the end of the left range, the start of the right range, and the number of element-to-pivot comparisons. Elements between those two ranges are already in place.
- `quicksort()` **recurses on the smaller range and loops over the larger one**. This keeps recursion depth small, even for unbalanced partitions.
- Each algorithm sorts a **copy of the same input**. `assert a == expected` checks correctness.
- `time.perf_counter()` measures runtime in **milliseconds**. Comparison counts are based on pivot comparisons; different partition methods can make different numbers of checks.
- `random.seed(42)` makes the random pivot sequence repeatable, while a separate seeded random generator creates test arrays.

## 3. Experiment

**Input sizes:** 1,000; 2,000; 4,000; 8,000; 16,000.

**Input types:** Random, already sorted, reverse sorted, and many duplicates (values 0–9).

The program prints results for **4 algorithms × 4 input types × 5 sizes = 80 tests**. The table below summarises the measured results at **16,000 elements**.

| Input | Variant | Comparisons | Time (ms) |
|---|---|---:|---:|
| Random | Lomuto | 257,076 | 12.713 |
| Random | Hoare | 331,514 | 18.900 |
| Random | Randomised | 252,241 | 14.873 |
| Random | Three-way | 411,331 | 24.129 |
| Sorted | Lomuto | 127,992,000 | 5002.070 |
| Sorted | Hoare | 252,884 | 14.671 |
| Sorted | Randomised | 287,590 | 13.656 |
| Sorted | Three-way | 320,745 | 18.914 |
| Reverse | Lomuto | 127,992,000 | 3863.205 |
| Reverse | Hoare | 252,830 | 14.807 |
| Reverse | Randomised | 265,360 | 14.471 |
| Reverse | Three-way | 319,712 | 19.782 |
| Duplicates | Lomuto | 12,863,723 | 500.236 |
| Duplicates | Hoare | 275,600 | 18.140 |
| Duplicates | Randomised | 12,852,504 | 499.608 |
| Duplicates | Three-way | 100,302 | 4.799 |

## 4. Which variants degrade to Θ(n²), and why?

- **Lomuto — sorted and reverse-sorted:** The last pivot is always the smallest or largest element, leaving partitions of sizes `0` and `n − 1`. This requires roughly `n(n − 1)/2` comparisons. It also performs poorly with many duplicates because equal elements repeatedly stay in partitions.
- **Randomised — many duplicates:** Although it picks random pivots, it still uses **two-way Lomuto partitioning**. Values equal to the pivot are not grouped together, creating repeatedly unbalanced partitions. Its *expected* behaviour with distinct values is Θ(n log n).
- **Hoare — no quadratic degradation in these tests:** The middle-pivot strategy gives balanced splits on sorted and reverse-sorted data, and Hoare partitioning handles equal values well. Its *worst case* is still Θ(n²) for other arrangements.
- **Three-way — no quadratic degradation in these tests:** Equal values form a middle group and are skipped during recursion, making it especially effective for duplicate-heavy input. An unlucky pivot choice can still cause Θ(n²) on other inputs.

## 5. Conclusion

**Lomuto** struggles with sorted, reverse-sorted, and duplicate-heavy inputs. **Randomised quicksort** improves the behaviour on ordered inputs but still struggles with many duplicates. **Hoare** performs consistently well across these tests, while **three-way quicksort** is the most efficient on the duplicate-heavy test.

Execution times depend on the computer and other running processes. Comparison counts are more useful for recognising the growth pattern of each algorithm.
