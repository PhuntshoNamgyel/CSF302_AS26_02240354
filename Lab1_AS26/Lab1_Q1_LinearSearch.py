def LinearSearch_354(data_354, target_354):
    for index_354 in range(len(data_354)):
        if data_354[index_354] == target_354:
            return index_354
    return -1


if __name__ == "__main__":
    sample_data_354 = [5, 3, 8, 1, 9, 2]
    target_354 = 9

    result_354 = LinearSearch_354(sample_data_354, target_354)

    if result_354 != -1:
        print(f"Element found at index {result_354}")
    else:
        print("Element not found")