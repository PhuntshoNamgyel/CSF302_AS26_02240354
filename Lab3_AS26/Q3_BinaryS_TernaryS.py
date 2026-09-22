import random

def generate_sorted_array_354(n, low=0, high=1000):
    array = sorted(random.sample(range(low, high), n)) if high - low >= n else sorted(random.choices(range(low, high), k=n))
    return array

def display_array_354(array):
    print(array)

def binary_search_354(array, key):
    low = 0
    high = len(array) - 1
    comparisons_354 = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons_354 += 1
        if array[mid] == key:
            return mid, comparisons_354
        elif array[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons_354

def ternary_search_354(array, key):
    low = 0
    high = len(array) - 1
    comparisons_354 = 0

    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        comparisons_354 += 1
        if array[mid1] == key:
            return mid1, comparisons_354

        comparisons_354 += 1
        if array[mid2] == key:
            return mid2, comparisons_354

        if key < array[mid1]:
            high = mid1 - 1
        elif key > array[mid2]:
            low = mid2 + 1
        else:
            low = mid1 + 1
            high = mid2 - 1

    return -1, comparisons_354

def best_case_354(array, search_func_354):
    n = len(array)
    mid = n // 2
    key = array[mid]
    index, comparisons_354 = search_func_354(array, key)
    return key, index, comparisons_354

def worst_case_354(array, search_func_354):
    if array:
        key = array[-1] + 1
    else:
        key = 0
    index, comparisons_354 = search_func_354(array, key)
    return key, index, comparisons_354

def comparison_table_354(sizes):
    print(f"{'n':>8} {'Binary (best)':>14} {'Binary (worst)':>15} {'Ternary (best)':>15} {'Ternary (worst)':>16}")
    for n in sizes:
        array = generate_sorted_array_354(n, low=0, high=n * 10)

        _, _, binary_best_354 = best_case_354(array, binary_search_354)
        _, _, binary_worst_354 = worst_case_354(array, binary_search_354)
        _, _, ternary_best_354 = best_case_354(array, ternary_search_354)
        _, _, ternary_worst_354 = worst_case_354(array, ternary_search_354)

        print(f"{n:>8} {binary_best_354:>14} {binary_worst_354:>15} {ternary_best_354:>15} {ternary_worst_354:>16}")

def print_menu_354():
    print("\n--- Menu ---")
    print("1. Generate n sorted random numbers")
    print("2. Display array")
    print("3. Search using Binary Search")
    print("4. Search using Ternary Search")
    print("5. Step count for best case")
    print("6. Step count for worst case")
    print("7. Step count comparison table across increasing n")
    print("8. Exit")

def main_354():
    array_354 = []

    while True:
        print_menu_354()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            n = int(input("Enter number of elements: "))
            array_354 = generate_sorted_array_354(n)
            print("Array generated.")

        elif choice == "2":
            if not array_354:
                print("Array is empty. Generate it first (option 1).")
            else:
                display_array_354(array_354)

        elif choice == "3":
            if not array_354:
                print("Array is empty. Generate it first (option 1).")
            else:
                key = int(input("Enter key to search: "))
                index, comparisons_354 = binary_search_354(array_354, key)
                if index != -1:
                    print(f"Found at index {index} in {comparisons_354} comparisons.")
                else:
                    print(f"Not found. Took {comparisons_354} comparisons.")

        elif choice == "4":
            if not array_354:
                print("Array is empty. Generate it first (option 1).")
            else:
                key = int(input("Enter key to search: "))
                index, comparisons_354 = ternary_search_354(array_354, key)
                if index != -1:
                    print(f"Found at index {index} in {comparisons_354} comparisons.")
                else:
                    print(f"Not found. Took {comparisons_354} comparisons.")

        elif choice == "5":
            if not array_354:
                print("Array is empty. Generate it first (option 1).")
            else:
                key_b, idx_b, comp_b = best_case_354(array_354, binary_search_354)
                key_t, idx_t, comp_t = best_case_354(array_354, ternary_search_354)
                print(f"Binary best case: key={key_b}, index={idx_b}, comparisons={comp_b}")
                print(f"Ternary best case: key={key_t}, index={idx_t}, comparisons={comp_t}")

        elif choice == "6":
            if not array_354:
                print("Array is empty. Generate it first (option 1).")
            else:
                key_b, idx_b, comp_b = worst_case_354(array_354, binary_search_354)
                key_t, idx_t, comp_t = worst_case_354(array_354, ternary_search_354)
                print(f"Binary worst case: key={key_b}, index={idx_b}, comparisons={comp_b}")
                print(f"Ternary worst case: key={key_t}, index={idx_t}, comparisons={comp_t}")

        elif choice == "7":
            sizes_354 = [10, 100, 1000, 10000, 100000]
            comparison_table_354(sizes_354)

        elif choice == "8":
            print("Exiting.")
            break

        else:
            print("Invalid choice. Try again.")

    # ------------------------- Analysis -------------------------
    # Recurrence relations:
    #   Binary Search  : T(n) = T(n/2) + O(1)   -> O(log2 n) comparisons
    #   Ternary Search : T(n) = T(n/3) + O(1)   -> O(log3 n) levels,
    #                                              2 comparisons per level
    #
    # Observation from the comparison table:
    #   - Binary Search needs fewer total comparisons than Ternary Search
    #     for the same n, in both best and worst cases.
    #   - Although Ternary Search divides the array into 3 parts and needs
    #     fewer levels (log3 n < log2 n), each level costs 2 comparisons
    #     instead of 1, making its total roughly 2 * log3 n.
    #   - Since log3 n is smaller than log2 n by only a constant factor,
    #     doubling the cost per level outweighs the benefit of fewer levels.
    #
    # Conclusion:
    #   Binary Search is generally more efficient than Ternary Search in
    #   terms of total comparisons made, even though it splits the search
    #   space into fewer parts per step.
    # ---------------------------------------------------------------

if __name__ == "__main__":
    main_354()