import random


def GenerateDataset_354(size_354):
    return [random.randint(1, size_354 * 10) for _ in range(size_354)]


if __name__ == "__main__":
    input_sizes_354 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]

    for size_354 in input_sizes_354:
        dataset_354 = GenerateDataset_354(size_354)
        print(f"Generated dataset of size {size_354}, first 5 elements: {dataset_354[:5]}")