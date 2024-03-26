def binary_insertion_sort(data):
    for i in range(1, len(data)):  ##
        key = data[i]
        lo, hi = 0, i  ##
        while lo < hi:
            mid = (lo + hi) // 2  ##
            if data[mid] < key:
                hi = mid
            else:
                lo = mid + 1
        for j in range(i, lo, -1):  ##
            print(i, lo, i, j)
            data[j] = data[j - 1]
        data[lo] = key
    return data


def binary_insertion_sort_desc(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        # binary search for correct position to insert x
        while j >= 0 and key > data[j]:
            j -= 1
        # shift elements to right to make space for x
        for k in range(i, j + 1, -1):
            data[k] = data[k - 1]
        # insert x in correct position
        data[j + 1] = key
    return data


a = [1, 3, 2, 4, 1, 5 ,0]
a = binary_insertion_sort(a)
print(a)
a = binary_insertion_sort_desc(a)
print(a)
