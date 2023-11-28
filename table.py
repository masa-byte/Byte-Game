import stack
import numpy as np


def is_row_in_middle(i, n):
    return i != 0 and i != n - 1


def is_field_black(i, j):
    return (i + j) % 2 == 0


def map_row_index_to_coin(i):
    return "W" if i % 2 == 0 else "B"


class Table:
    def __init__(self, n):
        self.n = n
        self.table = np.array(
            [[stack.WhiteField() for _ in range(n)] for _ in range(n)]
        )
        self.populate_table()

    def populate_table(self):
        for i in range(self.n):
            for j in range(self.n):
                if is_field_black(i, j):
                    self.table[i][j] = stack.Stack()
                    if is_row_in_middle(i, self.n):
                        coin = map_row_index_to_coin(i)
                        self.table[i][j].push(coin)

    def print_table(self):
        for i in range(self.n):
            matrix_row = []
            for j in range(self.n):
                matrix = self.table[i][j].print_field()
                matrix_row.append(matrix)

            for k in range(len(matrix_row[0][0])):
                row = ""
                for matrix in matrix_row:
                    row += "".join(matrix[k]) + " "
                print(row)
            print()

    def is_move_valid(self, move):
        return all(
            [
                move.is_direction_valid(),
                self.does_field_exist(self, move.i, move.j),
                self.does_coin_exist_on_stack_at_position(
                    self, move.i, move.j, move.coin_position_in_stack, move.coin_color
                ),
            ]
        )

    def does_field_exist(self, i, j):
        return is_field_black(i, j) if 0 <= i < self.n and 0 <= j < self.n else False

    def does_coin_exist_on_stack_at_position(self, i, j, coin_position_in_stack, coin_color):
        return self.table[i][j].does_coin_exist_at_position(
            coin_position_in_stack, coin_color
        )

    def is_table_empty(self):
        for i in range(self.n):
            for j in range(self.n):
                if is_field_black(i, j):
                    if not self.table[i][j].is_empty():
                        return False

        return True
