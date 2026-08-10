import random


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


if __name__ == "__main__":
    input_sizes_354 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]

    for size_354 in input_sizes_354:
        dataset_354 = GenerateDataset_354(size_354)
        sorted_dataset_354 = sorted(dataset_354)

        target_354 = sorted_dataset_354[size_354 // 2]
        result_354 = BinarySearch_354(sorted_dataset_354, target_354)

        print(f"Size {size_354}: target {target_354} found at index {result_354}")