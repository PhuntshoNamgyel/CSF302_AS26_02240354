
# Q2: Matrix Chain Multiplication

## 1. Bottom-Up Dynamic Programming

The bottom-up dynamic programming approach finds the minimum number of scalar multiplications required to multiply a chain of matrices.

It calculates the optimal cost for smaller matrix chains first and stores the results in a table. For each chain, it tries every possible split and selects the one with the lowest cost.

The time complexity is O(n³), and the space complexity is O(n²).

## 2. Optimal Parenthesisation

The program uses a split table to reconstruct the optimal multiplication order.

### Given Test Case 1

Dimensions: [30, 35, 15, 5, 10, 20, 25]

- Optimal Cost: 15,125
- Left-to-Right Cost: 40,500
- Optimal Parenthesisation: `((A1(A2A3))((A4A5)A6))`

The minimum cost matches the expected value of 15,125.

### Given Test Case 2

Dimensions: [5, 4, 6, 2, 7]

- Optimal Cost: 158
- Left-to-Right Cost: 250
- Optimal Parenthesisation: `((A1(A2A3))A4)`

## 3. Brute-Force Verification

The brute-force recursive approach tries every possible parenthesisation and returns the minimum multiplication cost.

It is used to verify the dynamic programming results for chains containing up to 8 matrices.

All seven test cases passed verification, confirming that the dynamic programming and brute-force approaches produce the same minimum costs.

## 4. Test Results

Five additional random matrix chains were generated using `random.seed(42)`.

| Test Case | Optimal Cost | Left-to-Right Cost | Verification |
|---|---:|---:|---|
| Given 1 | 15,125 | 40,500 | PASS |
| Given 2 | 158 | 250 | PASS |
| Random 1 | 1,550 | 4,000 | PASS |
| Random 2 | 3,842 | 27,125 | PASS |
| Random 3 | 1,422 | 4,122 | PASS |
| Random 4 | 22,680 | 30,456 | PASS |
| Random 5 | 15,670 | 20,048 | PASS |

## 5. Comparison

The left-to-right approach multiplies matrices sequentially without considering alternative multiplication orders.

Dynamic programming evaluates different parenthesisations and selects the one requiring the fewest scalar multiplications.

For the first test case, the left-to-right approach requires 40,500 multiplications, while the optimal approach requires only 15,125.

Brute-force recursion also finds the optimal cost but repeatedly evaluates overlapping subproblems, making it inefficient for larger chains.

## 6. Conclusion

All seven test cases produced matching results between bottom-up dynamic programming and brute-force recursion.

The optimal multiplication order consistently required fewer scalar multiplications than the left-to-right order in the tested cases.

Therefore, bottom-up dynamic programming is an efficient approach to matrix chain multiplication because it avoids repeated calculations and finds the minimum cost in O(n³) time.
