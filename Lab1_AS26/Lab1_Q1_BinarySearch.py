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


if __name__ == "__main__":
    sample_data_354 = [1, 2, 3, 5, 8, 9]
    target_354 = 8

    result_354 = BinarySearch_354(sample_data_354, target_354)

    if result_354 != -1:
        print(f"Element found at index {result_354}")
    else:
        print("Element not found")