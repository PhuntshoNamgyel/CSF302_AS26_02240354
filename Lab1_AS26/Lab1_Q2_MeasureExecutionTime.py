import random
import time


def BubbleSort_354(data_354):
    arr_354 = data_354.copy()
    n_354 = len(arr_354)

    for i_354 in range(n_354 - 1):
        for j_354 in range(n_354 - 1 - i_354):
            if arr_354[j_354] > arr_354[j_354 + 1]:
                arr_354[j_354], arr_354[j_354 + 1] = arr_354[j_354 + 1], arr_354[j_354]

    return arr_354


def MergeSort_354(data_354):
    if len(data_354) <= 1:
        return data_354

    mid_354 = len(data_354) // 2
    left_354 = MergeSort_354(data_354[:mid_354])
    right_354 = MergeSort_354(data_354[mid_354:])

    return Merge_354(left_354, right_354)


def Merge_354(left_354, right_354):
    result_354 = []
    i_354 = 0
    j_354 = 0

    while i_354 < len(left_354) and j_354 < len(right_354):
        if left_354[i_354] <= right_354[j_354]:
            result_354.append(left_354[i_354])
            i_354 += 1
        else:
            result_354.append(right_354[j_354])
            j_354 += 1

    result_354.extend(left_354[i_354:])
    result_354.extend(right_354[j_354:])

    return result_354


def GenerateArray_354(size_354):
    return [random.randint(1, size_354 * 10) for _ in range(size_354)]


def MeasureAverageTime_354(sort_func_354, array_354, num_runs_354=5):
    total_time_354 = 0

    for _ in range(num_runs_354):
        start_354 = time.perf_counter()
        sort_func_354(array_354)
        end_354 = time.perf_counter()
        total_time_354 += (end_354 - start_354)

    return total_time_354 / num_runs_354


if __name__ == "__main__":
    input_sizes_354 = [100, 500, 1000, 2000, 4000, 8000]

    print(f"{'Size':<12}{'Bubble Sort (s)':<20}{'Merge Sort (s)':<20}")
    print("-" * 52)

    for size_354 in input_sizes_354:
        array_354 = GenerateArray_354(size_354)

        bubble_time_354 = MeasureAverageTime_354(BubbleSort_354, array_354)
        merge_time_354 = MeasureAverageTime_354(MergeSort_354, array_354)

        print(f"{size_354:<12}{bubble_time_354:<20.8f}{merge_time_354:<20.8f}")