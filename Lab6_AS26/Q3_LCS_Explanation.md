
# Q3: Longest Common Subsequence (LCS)

## 1. Bottom-Up Dynamic Programming

The bottom-up dynamic programming approach finds the longest common subsequence between two strings.

Given:
- X = `ABCBDAB`
- Y = `BDCABA`

The program fills a table by comparing characters from both strings.

If the characters match, it adds 1 to the diagonal value. Otherwise, it takes the maximum value from the cell above or to the left.

### LCS Table

| X \ Y | - | B | D | C | A | B | A |
|---|---|---|---|---|---|---|---|
| - | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| B | 0 | 1 | 1 | 1 | 1 | 2 | 2 |
| C | 0 | 1 | 1 | 2 | 2 | 2 | 2 |
| B | 0 | 1 | 1 | 2 | 2 | 3 | 3 |
| D | 0 | 1 | 2 | 2 | 2 | 3 | 3 |
| A | 0 | 1 | 2 | 2 | 3 | 3 | 4 |
| B | 0 | 1 | 2 | 2 | 3 | 4 | 4 |

Time complexity: O(m × n)

Space complexity: O(m × n)

## 2. LCS Reconstruction

The program reconstructs one LCS by tracing backward through the completed DP table.

When matching characters are found, they are added to the subsequence. Otherwise, the program moves toward the cell with the larger value.

Results:
- LCS: `BCBA`
- LCS Length: 4

Other valid LCS sequences may exist with the same length.

## 3. Space-Optimised LCS

The space-optimised approach uses only two rows instead of storing the entire DP table.

One row stores the previous results, while the other stores the current calculations.

Results:
- Two-Row LCS Length: 4

Time complexity: O(m × n)

Space complexity: O(n), where n is the length of the second string.

This approach reduces memory usage while producing the same LCS length.

## 4. Performance Comparison

The program compares bottom-up dynamic programming with a brute-force approach that tries subsequences of X.

Random strings containing characters from `ABCD` were generated with lengths from 5 to 18.

### Execution Time (Milliseconds)

| Length | DP Time (ms) | Brute-Force Time (ms) |
|---|---:|---:|
| 5 | 0.0053 | 0.0094 |
| 6 | 0.0061 | 0.0124 |
| 7 | 0.0073 | 0.0656 |
| 8 | 0.0086 | 0.1295 |
| 9 | 0.0103 | 0.1460 |
| 10 | 0.0124 | 0.4584 |
| 11 | 0.0146 | 0.5148 |
| 12 | 0.0167 | 0.7643 |
| 13 | 0.0188 | 3.5313 |
| 14 | 0.0230 | 10.4623 |
| 15 | 0.0311 | 10.6345 |
| 16 | 0.0300 | 59.0379 |
| 17 | 0.0485 | 55.5507 |
| 18 | 0.0469 | 76.4150 |

The execution times were measured using Python's `perf_counter()` and may vary depending on system performance.

### Explanation

Dynamic programming solves overlapping subproblems once and stores their results, giving a time complexity of O(m × n).

The brute-force approach considers up to 2^m subsequences of X, resulting in exponential growth in the number of possibilities.

As the string length increases, the brute-force approach becomes significantly slower than dynamic programming.

## 5. Line-by-Line File Diff

The program compares two text files using LCS to identify unchanged, removed, and added lines.

### Output

    Hello
  - The cat sleeps
  + The dog sleeps
    Learning Python
  - Goodbye
  + See you

### Explanation

- Unchanged lines are part of the LCS and are displayed with a leading space.
- Lines beginning with `-` were removed from the original file.
- Lines beginning with `+` were added in the new file.

The LCS approach preserves common lines in their original relative order and identifies the differences between the two files.

## 6. Conclusion

The bottom-up dynamic programming approach successfully calculated the LCS length of 4 and reconstructed `BCBA`.

The two-row version produced the same length while reducing memory usage.

The performance comparison showed that dynamic programming is significantly faster than brute force for larger strings.

The LCS algorithm was also successfully applied to compare two text files and display their differences line by line.
