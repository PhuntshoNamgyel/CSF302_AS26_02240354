import random

def minmax354(arr354, lo354, hi354, comparisons354):
    if lo354 == hi354:
        return arr354[lo354], arr354[lo354]
    if hi354 == lo354 + 1:
        comparisons354[0] += 1
        if arr354[lo354] <= arr354[hi354]:
            return arr354[lo354], arr354[hi354]
        return arr354[hi354], arr354[lo354]
    mid354 = (lo354 + hi354) // 2
    min1_354, max1_354 = minmax354(arr354, lo354, mid354, comparisons354)
    min2_354, max2_354 = minmax354(arr354, mid354 + 1, hi354, comparisons354)
    comparisons354[0] += 1
    resultMin354 = min1_354 if min1_354 <= min2_354 else min2_354
    comparisons354[0] += 1
    resultMax354 = max1_354 if max1_354 >= max2_354 else max2_354
    return resultMin354, resultMax354


def run_trial354(n354):
    arr354 = [random.randint(0, 1000000) for _ in range(n354)]
    comparisons354 = [0]
    resultMin354, resultMax354 = minmax354(arr354, 0, n354 - 1, comparisons354)
    assert resultMin354 == min(arr354)
    assert resultMax354 == max(arr354)
    return comparisons354[0]


if __name__ == "__main__":
    sizes354 = [8, 64, 512, 4096]
    print(f"{'n':>6} {'Measured':>10} {'Predicted(3n/2-2)':>20} {'Two-scan(2n-2)':>16}")
    for n354 in sizes354:
        measured354 = run_trial354(n354)
        predicted354 = (3 * n354) // 2 - 2
        twoscan354 = 2 * n354 - 2
        print(f"{n354:>6} {measured354:>10} {predicted354:>20} {twoscan354:>16}")