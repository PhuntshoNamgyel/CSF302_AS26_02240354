def BubbleSort_354(data_354):
    n_354 = len(data_354)

    for i_354 in range(n_354 - 1):
        for j_354 in range(n_354 - 1 - i_354):
            if data_354[j_354] > data_354[j_354 + 1]:
                data_354[j_354], data_354[j_354 + 1] = data_354[j_354 + 1], data_354[j_354]

    return data_354


if __name__ == "__main__":
    sample_data_354 = [5, 3, 8, 1, 9, 2]

    sorted_data_354 = BubbleSort_354(sample_data_354)

    print(f"Sorted data: {sorted_data_354}")