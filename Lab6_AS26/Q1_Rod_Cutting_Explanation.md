
# Q1: Rod Cutting

## 1. Maximum Revenue and Optimal Cuts

The program calculates the maximum revenue for rod lengths 1 to 10 using the given price table.

| Rod Length (n) | Maximum Revenue | Optimal Pieces |
|---|---|---|
| 1 | 1 | [1] |
| 2 | 5 | [2] |
| 3 | 8 | [3] |
| 4 | 10 | [2, 2] |
| 5 | 13 | [2, 3] |
| 6 | 17 | [6] |
| 7 | 18 | [1, 6] |
| 8 | 22 | [2, 6] |
| 9 | 25 | [3, 6] |
| 10 | 30 | [10] |

## 2. Explanation of Approaches

### Naive Recursive Approach

The naive recursive approach tries every possible cut and recursively calculates the maximum revenue for the remaining rod. It repeatedly solves the same subproblems, resulting in exponential time complexity of O(2^n).

### Top-Down Memoization

The memoized approach uses recursion and stores previously calculated results in a cache. When the same subproblem occurs again, the stored result is reused instead of recalculated. This reduces the time complexity to O(n²).

### Bottom-Up Tabulation

The bottom-up approach calculates maximum revenues starting from smaller rod lengths using loops. It stores the results in a table and records the optimal cuts to reconstruct the piece lengths. Its time complexity is O(n²).

## 3. Performance Comparison

For rod lengths greater than 10, the price table is extended using p[i] = 3 × i.

### Recursive Call Counts

| n | Naive | Memoized | Bottom-Up |
|---|---:|---:|---:|
| 5 | 32 | 16 | 0 |
| 10 | 1,024 | 56 | 0 |
| 15 | 32,768 | 121 | 0 |
| 20 | 1,048,576 | 211 | 0 |
| 25 | 33,554,432 | 326 | 0 |

### Execution Time (Milliseconds)

| n | Naive | Memoized | Bottom-Up |
|---|---:|---:|---:|
| 5 | 0.013 | 0.007 | 0.003 |
| 10 | 0.290 | 0.014 | 0.006 |
| 15 | 8.907 | 0.024 | 0.011 |
| 20 | 278.115 | 0.033 | 0.013 |
| 25 | 6813.359 | 0.057 | 0.020 |

The execution times were measured using Python's `perf_counter()` and may vary depending on system performance.

## 4. Explanation of Differences

The naive recursive approach has the highest number of recursive calls because it repeatedly solves overlapping subproblems. Its execution time increases exponentially as the rod length increases.

Top-down memoization reduces repeated computations by storing calculated results. Although it still uses recursion, it requires significantly fewer calls than the naive approach.

Bottom-up tabulation uses iteration instead of recursion, resulting in zero recursive calls. It generally performs faster because it avoids recursion overhead.

## 5. Conclusion

All three approaches produce the same maximum revenue and optimal cuts. However, their performance differs significantly.

The naive recursive approach has O(2^n) time complexity, while both memoization and bottom-up tabulation have O(n²) time complexity.

Therefore, dynamic programming is more efficient for solving the rod cutting problem, especially for larger rod lengths.
