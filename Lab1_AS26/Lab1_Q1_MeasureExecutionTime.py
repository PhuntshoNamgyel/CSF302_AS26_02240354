import random
import time


def LinearSearch_354(data_354, target_354):
    for index_354 in range(len(data_354)):
        if data_354[index_354] == target_354:
            return index_354
    return -1


def BinarySearch_354(data_354, target_354):
    low_354 = 0
    high_354 = len(data_354) - 1

    while low_354 <= high_354:
        mid_354 = (low_354 + high_354) // 2
        if data_354[mid_354] == target_354:
            return mid_354
        elif data_354[mid_354] < target_354:
            low_354 = mid_354 + 1
        else:
            high_354 = mid_354 - 1

    return -1


def GenerateDataset_354(size_354):
    return [random.randint(1, size_354 * 10) for _ in range(size_354)]


def MeasureAverageTime_354(search_func_354, data_354, targets_354):
    start_354 = time.perf_counter()
    for target_354 in targets_354:
        search_func_354(data_354, target_354)
    end_354 = time.perf_counter()
    return (end_354 - start_354) / len(targets_354)


if __name__ == "__main__":
    input_sizes_354 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    num_targets_354 = 100

    print(f"{'Size':<12}{'Linear Search (s)':<22}{'Binary Search (s)':<22}")
    print("-" * 56)

    for size_354 in input_sizes_354:
        dataset_354 = GenerateDataset_354(size_354)
        sorted_dataset_354 = sorted(dataset_354)

        targets_354 = [random.choice(dataset_354) for _ in range(num_targets_354)]

        linear_time_354 = MeasureAverageTime_354(LinearSearch_354, dataset_354, targets_354)
        binary_time_354 = MeasureAverageTime_354(BinarySearch_354, sorted_dataset_354, targets_354)

        print(f"{size_354:<12}{linear_time_354:<22.8f}{binary_time_354:<22.8f}")