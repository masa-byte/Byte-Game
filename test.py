import numpy as np
import math


def diagonal_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_nearest_stacks_in_direction(i, j, visitied_fields):
    if does_field_exist(i, j):
        if not visitied_fields[i][j]:
            visitied_fields[i][j] = True
            if matrix[i][j] == 1:
                return (i, j)
            else:
                result = [0, 0, 0, 0]
                result[0] = find_nearest_stacks_in_direction(
                    i - 1,
                    j - 1,
                    visitied_fields,
                )
                result[1] = find_nearest_stacks_in_direction(
                    i - 1, j + 1, visitied_fields
                )
                result[2] = find_nearest_stacks_in_direction(
                    i + 1, j - 1, visitied_fields
                )
                result[3] = find_nearest_stacks_in_direction(
                    i + 1, j + 1, visitied_fields
                )

                result = list(filter(lambda x: x is not None, result))
                result.sort(key=lambda x: diagonal_distance((i, j), x))
                return result
    return None

def add_stack_if_exists(i, j, result):
    if does_field_exist(i, j):
        if matrix[i][j] == 1:
            result.add((i, j))


def find_nearest_stacks(i, j):
    result = set()

    for m in range(1, 8):
        for n in range(0, 2 * m + 1, 2):
            # gornja horizontala
            add_stack_if_exists(i - m, j - m + n, result)
            # leva vertikala
            add_stack_if_exists(i - m + n, j - m, result)
            # donja horizontala
            add_stack_if_exists(i + m, j - m + n, result)
            # desna vertikala
            add_stack_if_exists(i - m + n, j + m, result)
        if result:
            return result
    return result


def does_field_exist(i, j):
    return 0 <= i < 8 and 0 <= j < 8


if __name__ == "__main__":
    matrix = np.array([[0 for _ in range(8)] for _ in range(8)])
    matrix[3][3] = 1
    matrix[1][5] = 1
    matrix[3][5] = 1
    matrix[5][5] = 1
    
    result = find_nearest_stacks(3, 3)
    print(result)
