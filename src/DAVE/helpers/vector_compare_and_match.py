def vector_compare_and_match(vector1, vector2):
    """Compares two vectors where vector2 is an updated version of vector1 with
    - ONE element added or removed or
    - one element moved to a different position.
    - no changes at all

    The function returns at vector with the length of vector2 and aligned with the elements of vector2.
    The contents of the returned vector are the indices of the elements of vector1 that match that elements of vector2
    if any. If the element is not found in vector1, the index is None.

    If the input vectors are not as described above, the function returns None.

    """

    N1 = len(vector1)
    N2 = len(vector2)

    length_difference = N1 - N2
    if abs(length_difference) > 1:
        return None

    # no change at all
    if vector2 == vector1:
        return list(range(len(vector2)))

    i1 = 0
    result = list()

    for i2 in range(N2):

        if i1 >= N1:  # reached end of vector1
            break

        # elements match
        if vector2[i2] == vector1[i1]:
            result.append(i1)
            i1 += 1
            continue

        # does the next element in vector1 match?
        if i1+1 < N1 and vector2[i2] == vector1[i1+1]:
            result.append(i1+1)
            i1 += 2
            continue

        # no match
        result.append(None)  # forwards i2 but not i1

    if len(result) < N2:
        result.append(None)

    # if the vector2 is a re-oredered version of vector1, see if we can find the missing element
    if length_difference == 0 and None in result:
        # find the index of None in result

        missing_index = result.index(None)

        missing_value = vector2[missing_index]
        for i in range(N1):
            if i not in result:
                if vector1[i] == missing_value:
                    result[missing_index] = i
                    break

    # self-test
    for i in range(N2):
        if result[i] is not None:
            assert vector1[result[i]] == vector2[i]


    return result

if __name__ == '__main__':
    v1 = [1,2,3]
    v2 = [1,3]

    print(vector_compare_and_match(v1, v2))

    v1 = [1,3]
    v2 = [1,2,3]
    print(vector_compare_and_match(v1, v2))

    v1 = [1,2,3]
    v2 = [1,2,3]
    print(vector_compare_and_match(v1, v2))

    v1 = [1,2,3]
    v2 = [1,3,2]
    print(vector_compare_and_match(v1, v2))

    # two elements swapped (not supported)
    v1 = [3,2,1]
    v2 = [1,2,3]
    print(vector_compare_and_match(v1, v2))

    # inserted element
    v1 = [1,2,3]
    v2 = [1,2,4,3]
    print(vector_compare_and_match(v1, v2))

    # inserted element
    v1 = [1,2,3]
    v2 = [1,4,2,3]
    print(vector_compare_and_match(v1, v2))

    # inserted element
    v1 = [1,2,3]
    v2 = [4,1,2,3]
    print(vector_compare_and_match(v1, v2))

    # removed element
    v1 = [1,2,3,4]
    v2 = [1,2,4]
    print(vector_compare_and_match(v1, v2))

    # removed element
    v1 = [1,2,3,4]
    v2 = [1,2,3]
    print(vector_compare_and_match(v1, v2))

    # removed element
    v1 = [1,2,3,4]
    v2 = [1,3,4]
    print(vector_compare_and_match(v1, v2))

    # removed element
    v1 = [1,2,3,4]
    v2 = [2,3,4]
    print(vector_compare_and_match(v1, v2))








