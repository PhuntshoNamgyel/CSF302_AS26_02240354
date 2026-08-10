import random


def GenerateArray_354(size_354):
    return [random.randint(1, size_354 * 10) for _ in range(size_354)]


if __name__ == "__main__":
    input_sizes_354 = [100, 500, 1000, 2000, 4000, 8000]

    for size_354 in input_sizes_354:
        array_354 = GenerateArray_354(size_354)
        print(f"Generated array of size {size_354}, first 5 elements: {array_354[:5]}")