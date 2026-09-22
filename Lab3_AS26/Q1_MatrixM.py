import random
import time

def generate_matrix_354(n, low=0, high=9):
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]

def print_matrix_354(matrix, label=""):
    if label:
        print(label)
    for row in matrix:
        print(row)
    print()

def add_354(a, b):
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]

def sub_354(a, b):
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]

def traditional_mult_354(a, b):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += a[i][k] * b[k][j]
            result[i][j] = total
    return result

def split_354(matrix):
    n = len(matrix)
    mid = n // 2
    a11 = [row[:mid] for row in matrix[:mid]]
    a12 = [row[mid:] for row in matrix[:mid]]
    a21 = [row[:mid] for row in matrix[mid:]]
    a22 = [row[mid:] for row in matrix[mid:]]
    return a11, a12, a21, a22

def combine_354(c11, c12, c21, c22):
    top = [r1 + r2 for r1, r2 in zip(c11, c12)]
    bottom = [r1 + r2 for r1, r2 in zip(c21, c22)]
    return top + bottom

def strassen_mult_354(a, b):
    n = len(a)
    if n == 1:
        return [[a[0][0] * b[0][0]]]

    a11, a12, a21, a22 = split_354(a)
    b11, b12, b21, b22 = split_354(b)

    m1 = strassen_mult_354(add_354(a11, a22), add_354(b11, b22))
    m2 = strassen_mult_354(add_354(a21, a22), b11)
    m3 = strassen_mult_354(a11, sub_354(b12, b22))
    m4 = strassen_mult_354(a22, sub_354(b21, b11))
    m5 = strassen_mult_354(add_354(a11, a12), b22)
    m6 = strassen_mult_354(sub_354(a21, a11), add_354(b11, b12))
    m7 = strassen_mult_354(sub_354(a12, a22), add_354(b21, b22))

    c11 = add_354(sub_354(add_354(m1, m4), m5), m7)
    c12 = add_354(m3, m5)
    c21 = add_354(m2, m4)
    c22 = add_354(sub_354(add_354(m1, m3), m2), m6)

    return combine_354(c11, c12, c21, c22)

def compare_matrices_354(m1, m2):
    return m1 == m2

def run_comparison_354(n):
    matrix_a_354 = generate_matrix_354(n)
    matrix_b_354 = generate_matrix_354(n)

    start = time.perf_counter()
    result_traditional_354 = traditional_mult_354(matrix_a_354, matrix_b_354)
    time_traditional_354 = time.perf_counter() - start

    start = time.perf_counter()
    result_strassen_354 = strassen_mult_354(matrix_a_354, matrix_b_354)
    time_strassen_354 = time.perf_counter() - start

    match_354 = compare_matrices_354(result_traditional_354, result_strassen_354)

    return {
        "n": n,
        "traditional_time": time_traditional_354,
        "strassen_time": time_strassen_354,
        "match": match_354,
    }

def print_comparison_table_354(results):
    print(f"{'n':>5} {'Traditional (s)':>18} {'Strassen (s)':>15} {'Match':>7}")
    for stats in results:
        print(f"{stats['n']:>5} {stats['traditional_time']:>18.6f} {stats['strassen_time']:>15.6f} {str(stats['match']):>7}")

def main_354():
    n = 4
    matrix_a_354 = generate_matrix_354(n)
    matrix_b_354 = generate_matrix_354(n)

    print_matrix_354(matrix_a_354, "Matrix A:")
    print_matrix_354(matrix_b_354, "Matrix B:")

    result_traditional_354 = traditional_mult_354(matrix_a_354, matrix_b_354)
    result_strassen_354 = strassen_mult_354(matrix_a_354, matrix_b_354)

    print_matrix_354(result_traditional_354, "Result (Traditional):")
    print_matrix_354(result_strassen_354, "Result (Strassen):")

    match_354 = compare_matrices_354(result_traditional_354, result_strassen_354)
    print(f"Results match: {match_354}\n")

    sizes_354 = [2, 4, 8, 16, 32, 64]
    results_354 = [run_comparison_354(size) for size in sizes_354]

    print("Timing comparison across sizes:")
    print_comparison_table_354(results_354)

    # ------------------------- Analysis -------------------------
    # Time Complexity:
    #   Traditional Method : O(n^3)      (triple nested loop)
    #   Strassen's Method  : O(n^2.81)   (7 multiplications per split)
    #
    # Observation from the timing table:
    #   - For small n (2, 4, 8), Strassen's is slower than Traditional.
    #     This is because of the extra matrix additions/subtractions and
    #     recursive function call overhead needed at each split.
    #   - As n grows larger, Strassen's growth rate is slower than
    #     Traditional's, so the gap would close and eventually reverse
    #     for sufficiently large n.
    #
    # Correctness:
    #   Both methods produced identical results for every tested size,
    #   confirming the Strassen implementation is correct.
    #
    # Conclusion:
    #   Strassen's algorithm is asymptotically faster, but its benefit
    #   only becomes visible at large matrix sizes. For small inputs,
    #   the simpler Traditional method is more practical.
    # ---------------------------------------------------------------

if __name__ == "__main__":
    main_354()