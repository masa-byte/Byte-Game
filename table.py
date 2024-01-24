import stack
import numpy as np
from directions import Direction
from move import Move


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
                    self.table[i][j] = stack.BlackField()
                    if is_row_in_middle(i, self.n):
                        coin = map_row_index_to_coin(i)
                        self.table[i][j].push([coin])

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
                print(str(i) + " " + row)
            print()

    def is_move_valid(self, move):
        if move.is_direction_valid():
            if self.does_field_exist(move.i, move.j):
                if self.does_coin_exist_on_stack_at_position(
                    move.i, move.j, move.coin_position_in_stack, move.coin_color
                ):
                    return True
        return False

    def add_directions_in_result_if_exists(self, i, j, result, valid_moves):
        if self.does_field_exist(i, j):
            if not self.table[i][j].is_empty():
                result.update(valid_moves)
        return False

    def check_diagonals(self, i, j, m, result):
        # tl
        self.add_directions_in_result_if_exists(i - m, j - m, result, [Direction.TL])
        # tr
        self.add_directions_in_result_if_exists(i - m, j + m, result, [Direction.TR])
        # bl
        self.add_directions_in_result_if_exists(i + m, j - m, result, [Direction.BL])
        # br
        self.add_directions_in_result_if_exists(i + m, j + m, result, [Direction.BR])

    def check_middles(self, i, j, m, n, result):
        # top horizontal
        self.add_directions_in_result_if_exists(
            i - m, j - m + n, result, [Direction.TL, Direction.TR]
        )
        # left vertical
        self.add_directions_in_result_if_exists(
            i - m + n, j - m, result, [Direction.TL, Direction.BL]
        )
        # bottom horizontal
        self.add_directions_in_result_if_exists(
            i + m, j - m + n, result, [Direction.BL, Direction.BR]
        )
        # right vertical
        self.add_directions_in_result_if_exists(
            i - m + n, j + m, result, [Direction.TR, Direction.BR]
        )

    def find_allowed_directions(self, i, j):
        result = set()

        for m in range(1, self.n):
            self.check_diagonals(i, j, m, result)

            for n in range(2, 2 * m - 1, 2):
                self.check_middles(i, j, m, n, result)

            if result:
                return result

        return result

    def get_vicinity_stacks(self, i, j):
        result = []
        # top left
        if (
            self.does_field_exist(i - 1, j - 1)
            and not self.table[i - 1][j - 1].is_empty()
        ):
            result.append(self.table[i - 1][j - 1])
        # top right
        if (
            self.does_field_exist(i - 1, j + 1)
            and not self.table[i - 1][j + 1].is_empty()
        ):
            result.append(self.table[i - 1][j + 1])
        # bottom right
        if (
            self.does_field_exist(i + 1, j + 1)
            and not self.table[i + 1][j + 1].is_empty()
        ):
            result.append(self.table[i + 1][j + 1])
        # bottom left
        if (
            self.does_field_exist(i + 1, j - 1)
            and not self.table[i + 1][j - 1].is_empty()
        ):
            result.append(self.table[i + 1][j - 1])
        return result

    def get_destination_stack(self, i, j, direction):
        if direction == Direction.TL.value and (i - 1) >= 0 and (j - 1) >= 0:
            return [self.table[i - 1][j - 1], i - 1, j - 1]
        elif direction == Direction.TR.value and (i - 1) >= 0 and (j + 1) < self.n:
            return [self.table[i - 1][j + 1], i - 1, j + 1]
        elif direction == Direction.BL.value and (i + 1) < self.n and (j - 1) >= 0:
            return [self.table[i + 1][j - 1], i + 1, j - 1]
        elif direction == Direction.BR.value and (i + 1) < self.n and (j + 1) < self.n:
            return [self.table[i + 1][j + 1], i + 1, j + 1]
        return None

    def is_moving_part_of_stack_allowed(self, i, j, move):
        source_stack = self.table[i][j]
        height_of_source_stack = source_stack.get_number_of_coins()

        destination_stack = self.get_destination_stack(i, j, move.direction)
        if destination_stack is None:
            return False
        
        destination_stack = destination_stack[0]

        height_of_destination_stack = destination_stack.get_number_of_coins()

        num_of_coins_to_move = source_stack.get_number_of_coins_from_position(
            move.coin_position_in_stack
        )

        if (
            height_of_destination_stack + num_of_coins_to_move
            <= destination_stack.capacity
        ):
            if height_of_destination_stack == 0 and num_of_coins_to_move == height_of_source_stack:
                return True
            if (
                height_of_destination_stack + num_of_coins_to_move
                > height_of_source_stack
            ):
                return True
        return False

    def is_move_allowed(self, move):
        i = move.i
        j = move.j
        result = self.find_allowed_directions(i, j)
        if move.direction in map(lambda el: el.value, result):
            return self.is_moving_part_of_stack_allowed(i, j, move)
        return False

    def does_field_exist(self, i, j):
        return is_field_black(i, j) if 0 <= i < self.n and 0 <= j < self.n else False

    def does_coin_exist_on_stack_at_position(
        self, i, j, coin_position_in_stack, coin_color
    ):
        return self.table[i][j].does_coin_exist_at_position(
            coin_position_in_stack, coin_color
        )

    def is_table_empty(self):
        return all(
            [
                self.table[i][j].is_empty()
                for i in range(self.n)
                for j in range(self.n)
                if is_field_black(i, j)
            ]
        )

    def play_move(self, move):
        i = move.i
        j = move.j
        source_stack = self.table[i][j]
        destination_stack = self.get_destination_stack(i, j, move.direction)
        destination_stack = destination_stack[0]
        coins_to_move = source_stack.pop(move.coin_position_in_stack)
        destination_stack.push(coins_to_move)

        if destination_stack.get_number_of_coins() == destination_stack.capacity:
            destination_stack.pop(0)
            return coins_to_move[-1]
        return None

    def get_all_allowed_moves(self, color):
        result = []
        for i in range(self.n):
            for j in range(self.n):
                if is_field_black(i, j):
                    for coin_position_in_stack in range(
                        self.table[i][j].get_number_of_coins()
                    ):
                        if self.table[i][j].elements[coin_position_in_stack] == color:
                            for direction in Direction:
                                move = Move(
                                    i, j, coin_position_in_stack, direction.value, color
                                )
                                if self.is_move_allowed(move):
                                    result.append(move)
        return result
