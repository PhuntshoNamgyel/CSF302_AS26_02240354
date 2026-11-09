
# Q3: Counting Inversions

## 1. Introduction

An inversion is a pair of elements (i, j) where i < j but A[i] > A[j].

Inversions measure how far an array is from being sorted.

### Example

Array: [3, 1, 2]

Inversions:
- (3, 1)
- (3, 2)

Total inversions: 2

A sorted array has zero inversions. A reverse-sorted array containing distinct elements has the maximum number of inversions.

## 2. Brute-Force Inversion Count

Brute force counts inversions by checking every possible pair of elements.

### How It Works

1. Select an element at index i.
2. Compare it with every element at a later index j.
3. If A[i] > A[j], increase the inversion count.
4. Repeat until all pairs have been checked.

### Time Complexity

- Time: Θ(n²)
- Auxiliary space: O(1)

Brute force is simple but inefficient for large arrays because the number of comparisons grows quadratically.

## 3. Merge-Sort-Based Inversion Count

This algorithm uses the divide-and-conquer approach from merge sort.

Instead of checking every pair individually, it counts multiple inversions while merging sorted halves.

### How It Works

1. Divide the array into two halves.
2. Recursively count inversions in each half.
3. Merge the sorted halves.
4. Count cross inversions during merging.
5. Add the inversion counts from both halves and the merge step.

### Important Logic

`count += mid - i`

When the current right-half element is smaller than the current left-half element, all remaining left-half elements are also greater.

Therefore, `mid - i` inversions can be counted at once.

The comparison uses `<=` so equal elements are not counted as inversions.

### Time Complexity

- Time: Θ(n log n)
- Auxiliary space: O(n)

The merge-sort approach is more efficient because it counts multiple inversions during a single merge operation.

## 4. Important Code Explanation

### brute_force_inversions()

- `count` stores the total inversion count.
- Nested loops check every pair where i < j.
- `data[i] > data[j]` identifies an inversion.
- `time_limit` stops execution when the allowed time is reached.

### merge_sort_inversions()

- `values` creates a copy of the original array.
- `temp` temporarily stores elements during merging.
- `sort(lo, hi)` recursively divides the array.
- `count += mid - i` counts cross inversions.
- Returns the sorted array and total inversion count.

### verify_algorithms()

- Tests random arrays up to 2,000 elements.
- Includes empty arrays, duplicates, and negative values.
- Compares the inversion counts from both methods.
- Uses `assert` to verify correctness.

### benchmark()

- Tests input sizes from 1,000 to 1,000,000.
- Measures execution time using `time.perf_counter()`.
- Stops brute force after reaching the 60-second limit.
- Continues merge-sort counting for all input sizes.

### plot_results()

- Plots the execution times of both algorithms.
- Uses logarithmic scales to show performance differences.
- Shows the 60-second cutoff.
- Saves the graph as `q3_inversion_plot.png`.

### movie_rankings()

- Accepts 10 movie titles and two rankings from the keyboard.
- Converts User A's ranking into positions in User B's ranking.
- Counts inversions to calculate Kendall tau distance.
- Calculates ranking similarity and Kendall tau correlation.

## 5. Correctness Verification

Both algorithms were tested on random arrays of sizes:

10, 100, 500, 1,000, and 2,000.

Additional tests included empty arrays, single elements, and duplicate values.

### Worked Example

Input: [5, 2, 6, 1, 3, 4]

Inversions:
- (5, 2), (5, 1), (5, 3), (5, 4)
- (2, 1)
- (6, 1), (6, 3), (6, 4)

Total inversions: 8

### Verification Result

Both brute-force and merge-sort-based methods returned identical inversion counts for all tested arrays.

## 6. Experimental Results

The following results were obtained by running the program on my MacBook Air M3.

Execution times are measured in seconds.

### Brute Force vs Merge-Sort Inversion Count

| n | Brute Force (s) | Merge Sort (s) |
|---:|---:|---:|
| 1,000 | 0.017 | 0.001 |
| 2,000 | 0.064 | 0.002 |
| 4,000 | 0.251 | 0.005 |
| 8,000 | 0.991 | 0.011 |
| 16,000 | 3.964 | 0.023 |
| 32,000 | 16.006 | 0.049 |
| 64,000 | Stopped (>60s) | 0.105 |
| 128,000 | Skipped | 0.222 |
| 256,000 | Skipped | 0.472 |
| 512,000 | Skipped | 0.993 |
| 1,000,000 | Skipped | 2.061 |

**Graph:** `q3_inversion_plot.png`

## 7. Results Analysis

### Brute Force

Brute force became significantly slower as the input size increased.

At n = 1,000, it took only 0.017 seconds, but at n = 32,000, it required 16.006 seconds.

At n = 64,000, execution reached the 60-second limit and was stopped.

This behaviour is consistent with Θ(n²) time complexity because brute force examines every possible pair.

Doubling the input size approximately quadruples the execution time.

### Merge-Sort-Based Counting

Merge sort performed efficiently across all tested input sizes.

At n = 32,000, it completed in only 0.049 seconds, compared with brute force's 16.006 seconds.

Even at n = 1,000,000, merge sort required only 2.061 seconds.

This is consistent with Θ(n log n) time complexity.

The algorithm avoids unnecessary comparisons by counting multiple cross inversions during merging.

### Comparison

Brute force is easier to implement but becomes impractical for large inputs.

Merge-sort-based counting requires more implementation logic and O(n) auxiliary space but scales much better.

The experimental results demonstrate the performance advantage of the divide-and-conquer approach.

## 8. Kendall Tau Distance

Kendall tau distance measures the number of pairs ordered differently between two rankings.

The program compares two users' rankings of the same 10 Marvel movies.

### Movie List

| ID | Movie |
|---:|---|
| 1 | Avengers: Endgame |
| 2 | Avengers: Infinity War |
| 3 | Avengers: Age of Ultron |
| 4 | The Avengers |
| 5 | Iron Man |
| 6 | Captain America: Civil War |
| 7 | Spider-Man: No Way Home |
| 8 | Thor: Ragnarok |
| 9 | Black Panther |
| 10 | Doctor Strange |

### User Rankings

User A (best to worst):

1 2 3 4 5 6 7 8 9 10

User B (best to worst):

2 1 4 3 6 5 8 7 10 9

### Calculation

Total possible movie pairs:

10 × 9 / 2 = 45

The rankings disagree on five pairs:

- Movies 1 and 2
- Movies 3 and 4
- Movies 5 and 6
- Movies 7 and 8
- Movies 9 and 10

Therefore:

Kendall tau distance = 5 / 45

Ranking similarity:

(45 - 5) / 45 × 100 = 88.89%

Kendall tau correlation:

1 - (2 × 5 / 45) = 0.778

### Results

| Metric | Result |
|---|---:|
| Kendall tau distance | 5 / 45 |
| Ranking similarity | 88.89% |
| Kendall tau correlation | 0.778 |

### Interpretation

The two users disagree on only 5 out of 45 possible movie pairs.

They agree on the remaining 40 pairs, giving an agreement percentage of 88.89%.

The Kendall tau correlation of 0.778 indicates strong positive agreement between their rankings.

A smaller Kendall tau distance indicates more similar rankings.

## 9. Conclusion

The experiment demonstrates that brute-force inversion counting is simple but inefficient for large inputs due to its Θ(n²) time complexity.

Merge-sort-based inversion counting improves performance to Θ(n log n) by counting multiple cross inversions during merging.

Both algorithms returned identical counts during verification, confirming their correctness.

The benchmark showed that merge sort could process 1,000,000 elements in 2.061 seconds, while brute force exceeded the 60-second limit at 64,000 elements.

The Kendall tau example demonstrated a practical application of inversion counting, producing a distance of 5 and a ranking agreement of 88.89%.

Overall, merge-sort-based inversion counting is more suitable for large datasets and ranking comparisons.
