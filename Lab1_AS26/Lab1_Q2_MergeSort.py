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


if __name__ == "__main__":
    sample_data_354 = [5, 3, 8, 1, 9, 2]

    sorted_data_354 = MergeSort_354(sample_data_354)

    print(f"Sorted data: {sorted_data_354}")