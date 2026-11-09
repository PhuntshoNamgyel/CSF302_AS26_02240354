
# Q2: Counting Sort and Radix Sort

## 1. Counting Sort

Counting sort is a non-comparison sorting algorithm that sorts non-negative integers by counting how many times each key appears.

### How It Works

1. Create a count array for keys from 0 to k.
2. Count how many times each key appears.
3. Convert the frequencies into cumulative counts.
4. Place elements into their correct sorted positions.
5. Process elements backwards to preserve the order of equal keys.

### Time Complexity

- Time: Θ(n + k)
- Space: Θ(n + k)

Counting sort is efficient when the key range k is small. However, a large k increases the time and memory required for the count array.

## 2. LSD Radix Sort

LSD (Least Significant Digit) radix sort sorts integers digit by digit, starting from the rightmost digit.

It uses stable counting sort for each digit to preserve the ordering established by previous passes.

### Base 10

- Uses decimal digits from 0 to 9.
- Sorts numbers one digit at a time.
- Numbers up to 10^9 require at most 10 passes.

### Base 256

- Uses digit values from 0 to 255.
- Processes 8 bits per pass.
- Numbers up to 10^9 require at most 4 passes.

### Time Complexity

- Time: Θ(d(n + b))
- Space: Θ(n + b)

Where:
- n = Number of elements
- d = Number of digit passes
- b = Base used for sorting

Base 256 generally performs faster because it requires fewer digit passes than base 10.

## 3. Merge Sort (Lab 1)

The original `MergeSort_354()` and `Merge_354()` functions from Lab 1 are used for comparison.

Merge sort is a comparison-based sorting algorithm that follows the divide-and-conquer approach.

### How It Works

1. Divide the array into two halves.
2. Recursively sort each half.
3. Merge the sorted halves into one sorted array.

### Time Complexity

- Time: Θ(n log n)
- Space: O(n) auxiliary storage

Unlike counting sort, merge sort's time complexity does not depend on the maximum key value.

## 4. Important Code Explanation

### counting_sort()

- `count` stores how many times each key appears.
- Cumulative counts determine the final positions of elements.
- `reversed(items)` processes elements backwards to maintain stability.
- The `key` function allows sorting integers or `(key, index)` pairs.

### radix_sort()

- `place` identifies the current digit position.
- `(x // place) % base` extracts the digit being processed.
- Stable counting sort arranges elements by the current digit.
- `place *= base` moves to the next digit position.

### MergeSort_354()

- Divides the array into two smaller halves.
- Recursively sorts both halves.
- Calls `Merge_354()` to combine the sorted halves.

### Merge_354()

- Compares elements from the left and right halves.
- Adds the smaller element to the result.
- Appends any remaining elements after one half is exhausted.

### measure()

- `time.perf_counter()` measures execution time.
- Execution time is converted into milliseconds.
- `assert` verifies that the sorting result is correct.

### benchmark_counting()

- Keeps n fixed at 100,000.
- Tests k = 10, 1,000, 100,000, and 10,000,000.
- Compares counting sort with merge sort.
- Generates `q2_counting_plot.png`.

### benchmark_radix()

- Keeps k fixed at 10^9.
- Tests n = 10,000; 50,000; 100,000; 500,000; and 1,000,000.
- Compares radix sort (base 10), radix sort (base 256), and merge sort.
- Generates `q2_radix_plot.png`.

## 5. Stability Demonstration

Counting sort is stable because it preserves the original relative order of elements with equal keys.

Each pair contains `(key, original index)`.

### Original Input

```text
[(3, 0), (1, 1), (3, 2), (2, 3), (1, 4), (3, 5)]
```

### Sorted Output

```text
[(1, 1), (1, 4), (2, 3), (3, 0), (3, 2), (3, 5)]
```

### Explanation

- For key 1, the original indices remain 1 and 4.
- For key 3, the original indices remain 0, 2, and 5.
- Elements with equal keys maintain their original relative order.

Therefore, the counting sort implementation is stable.

## 6. Experimental Results

The following results were obtained by running the program on my MacBook Air M3.

Execution times are measured in milliseconds (ms).

### Experiment A: Counting Sort vs Merge Sort

Fixed input size: n = 100,000.

| k | Counting Sort (ms) | Merge Sort (ms) |
|---:|---:|---:|
| 10 | 13.382 | 136.935 |
| 1,000 | 14.075 | 151.143 |
| 100,000 | 20.109 | 147.539 |
| 10,000,000 | 687.190 | 148.265 |

**Graph:** `q2_counting_plot.png`

### Experiment B: Radix Sort vs Merge Sort

Fixed maximum key: k = 10^9.

| n | Base 10 (ms) | Base 256 (ms) | Merge Sort (ms) |
|---:|---:|---:|---:|
| 10,000 | 16.971 | 7.600 | 12.423 |
| 50,000 | 86.349 | 37.409 | 70.423 |
| 100,000 | 171.306 | 76.062 | 150.283 |
| 500,000 | 891.409 | 398.232 | 836.600 |
| 1,000,000 | 1886.452 | 841.906 | 1778.580 |

**Graph:** `q2_radix_plot.png`

## 7. Results Analysis

### Counting Sort

Counting sort performed faster than merge sort when the key range was small.

At k = 10, counting sort took only 13.382 ms, compared with merge sort's 136.935 ms.

However, at k = 10,000,000, counting sort took 687.190 ms, while merge sort took only 148.265 ms.

This happens because counting sort has Θ(n + k) complexity. As k increases, creating and processing the count array requires more time and memory.

Therefore, counting sort wins when the key range is relatively small but loses when k becomes very large.

### Radix Sort

Radix sort with base 256 performed fastest across all tested input sizes.

At n = 1,000,000:

- Base 10: 1886.452 ms
- Base 256: 841.906 ms
- Merge sort: 1778.580 ms

Base 256 performed better because it processes more bits per pass and requires fewer passes than base 10.

Base 10 was slower than merge sort at every tested input size because its repeated digit-sorting passes introduced additional processing overhead.

Therefore, radix sort wins when the number of passes and their processing costs are sufficiently small.

### Merge Sort

Merge sort maintained consistent performance as the key range increased.

Its Θ(n log n) complexity depends on the number of elements rather than the maximum key value.

It outperformed counting sort at k = 10,000,000 and radix sort with base 10 across all tested input sizes.

However, radix sort with base 256 was faster than merge sort in every test.

Merge sort remains a reliable general-purpose algorithm because its performance does not depend on the key range.

## 8. Conclusion

The experiment demonstrates that the efficiency of sorting algorithms depends on the input size, key range, and algorithm overhead.

Counting sort performs well when the key range is small but becomes inefficient when k is very large.

Radix sort with base 256 achieved the best performance in the second experiment because it required fewer digit passes than base 10.

Merge sort provided reliable performance regardless of the key range, while radix sort with base 10 was slower due to additional processing overhead.

The stability test also confirmed that counting sort preserves the original order of elements with equal keys.

Overall, linear-time sorting algorithms can outperform merge sort when their key-range and digit-processing costs remain manageable.
