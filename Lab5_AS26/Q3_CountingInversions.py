
import random
import time


def brute_force_inversions(data, time_limit=None):
    count = 0
    start = time.perf_counter()
    n = len(data)

    # Check every pair (i, j) where i < j.
    for i in range(n - 1):
        # Stop if the time limit has been reached.
        if time_limit is not None and time.perf_counter() - start >= time_limit:
            return None

        for j in range(i + 1, n):
            if data[i] > data[j]:
                count += 1

    return count


def merge_sort_inversions(data):
    # Merge sort with inversion counting during merging.
    values = data.copy()
    temp = [0] * len(values)

    def sort(lo, hi):
        if hi - lo <= 1:
            return 0

        # Divide the array and count inversions in both halves.
        mid = (lo + hi) // 2
        count = sort(lo, mid) + sort(mid, hi)
        i, j, pos = lo, mid, lo

        # Merge sorted halves and count cross inversions.
        while i < mid and j < hi:
            if values[i] <= values[j]:
                temp[pos] = values[i]
                i += 1
            else:
                temp[pos] = values[j]
                j += 1

                # Every remaining left element is greater.
                count += mid - i

            pos += 1

        # Copy remaining elements from either half.
        while i < mid:
            temp[pos] = values[i]
            i += 1
            pos += 1

        while j < hi:
            temp[pos] = values[j]
            j += 1
            pos += 1

        values[lo:hi] = temp[lo:hi]
        return count

    return values, sort(0, len(values))


def verify_algorithms():
    rng = random.Random(42)

    # Include edge cases, duplicates, and a worked example.
    examples = [
        [], [5], [2, 1], [1, 1],
        [3, 1, 2], [5, 2, 6, 1, 3, 4]
    ]

    # Test random arrays up to 2,000 elements.
    for n in [10, 100, 500, 1000, 2000]:
        for _ in range(3):
            examples.append([rng.randint(-10, 10) for _ in range(n)])

    for data in examples:
        brute = brute_force_inversions(data)
        sorted_data, merge = merge_sort_inversions(data)

        assert brute == merge, "Inversion counts do not match"
        assert sorted_data == sorted(data), "Incorrect sorting result"

    print("VERIFICATION: Both methods agree for arrays up to 2,000 elements.\n")


def benchmark():
    rng = random.Random(42)

    sizes = [
        1000, 2000, 4000, 8000, 16000, 32000,
        64000, 128000, 256000, 512000, 1000000
    ]

    brute_sizes = []
    brute_times = []
    merge_times = []
    brute_enabled = True

    print("INVERSION COUNT BENCHMARK")
    print(f'{"n":>10} {"Brute (s)":>14} {"Merge (s)":>14}')

    for n in sizes:
        # Generate identical input data for both algorithms.
        data = [rng.randint(0, n) for _ in range(n)]

        # Measure merge-sort-based inversion counting.
        start = time.perf_counter()
        sorted_data, fast_count = merge_sort_inversions(data)
        merge_seconds = time.perf_counter() - start

        merge_times.append(merge_seconds)
        assert sorted_data == sorted(data)

        if brute_enabled:
            start = time.perf_counter()
            brute_count = brute_force_inversions(data, time_limit=60)
            brute_seconds = time.perf_counter() - start

            if brute_count is None:
                # Stop testing brute force for larger input sizes.
                brute_enabled = False
                brute_result = "Stopped (>60s)"
            else:
                assert brute_count == fast_count
                brute_sizes.append(n)
                brute_times.append(brute_seconds)
                brute_result = f"{brute_seconds:.3f}"
        else:
            brute_result = "Skipped"

        print(
            f"{n:>10,} {brute_result:>14} "
            f"{merge_seconds:>14.3f}",
            flush=True
        )

    return sizes, brute_sizes, brute_times, merge_times


def plot_results(sizes, brute_sizes, brute_times, merge_times):
    import matplotlib.pyplot as plt

    # Plot both algorithms and the 60-second time limit.
    plt.figure(figsize=(8, 5))
    plt.plot(brute_sizes, brute_times, 'o-', label="Brute force")
    plt.plot(sizes, merge_times, 's-', label="Merge sort")
    plt.axhline(60, color='gray', linestyle='--', label="60-second limit")

    # Log scales make large differences in execution time easier to see.
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Input size n (log scale)")
    plt.ylabel("Time (seconds, log scale)")
    plt.title("Brute force vs merge-sort inversion count")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig("q3_inversion_plot.png", dpi=160)
    plt.close()

    print("\nPlot saved: q3_inversion_plot.png\n")


def movie_rankings():
    print("MOVIE RANKING COMPARISON (10 MOVIES)")
    movies = []

    # Enter 10 unique movie titles.
    while len(movies) < 10:
        title = input(f"Movie {len(movies) + 1}: ").strip()

        if not title or title.casefold() in [m.casefold() for m in movies]:
            print("Enter a non-empty, unique movie title.")
            continue

        movies.append(title)

    print("\nMovie IDs:")
    for i, title in enumerate(movies, 1):
        print(f"{i}. {title}")

    def read_ranking(user):
        while True:
            raw = input(f"\n{user} ranking (10 IDs, best to worst): ")

            try:
                ranking = [int(x) for x in raw.split()]
            except ValueError:
                print("Enter 10 movie ID numbers separated by spaces.")
                continue

            # Each movie must appear exactly once.
            if sorted(ranking) == list(range(1, 11)):
                return ranking

            print("Enter each movie ID from 1 to 10 exactly once.")

    rank_a = read_ranking("User A")
    rank_b = read_ranking("User B")

    # Convert A's ranking into positions in B's ranking.
    position_b = {movie: i for i, movie in enumerate(rank_b)}
    sequence = [position_b[movie] for movie in rank_a]

    # Each inversion represents a pair ranked differently.
    _, distance = merge_sort_inversions(sequence)

    total_pairs = 10 * 9 // 2  # 45 possible movie pairs.
    similarity = (total_pairs - distance) / total_pairs * 100
    tau = 1 - 2 * distance / total_pairs

    print(f"\nKendall tau distance: {distance} / {total_pairs}")
    print(f"Ranking similarity: {similarity:.2f}%")
    print(f"Kendall tau correlation: {tau:.3f}")


if __name__ == "__main__":
    verify_algorithms()
    results = benchmark()
    plot_results(*results)
    movie_rankings()
