import table
import move
from math import ceil


class Game:
    def __init__(self, human_first, table_dimension):
        self.human_first = True if human_first == "1" else False
        self.table_dimension = table_dimension
        self.game_table = table.Table(table_dimension)
        self.game_table.print_table()

        self.white_stacks = 0
        self.black_stacks = 0

    def get_valid_move(self):
        while True:
            print("Enter i, j, coin_position_in_stack, direction")
            print("Valid directions: TL, TR, BL, BR")
            splited_input = input("Enter move: ").split()
            if len(splited_input) == 4:
                c = 0
                i = splited_input[c]
                c += 1
                j = splited_input[c]
                c += 1
                coin_position_in_stack = splited_input[c]
                c += 1
                direction = splited_input[c]
                c += 1

                if i.isnumeric() and j.isnumeric():
                    player_move = move.Move(int(i), int(j), int(coin_position_in_stack), direction)
                    outcome = self.game_table.is_move_valid(player_move)
                    if outcome:
                        return player_move

    def is_game_over(self):
        if (
            self.game_table.is_table_empty()
            or self.white_stacks >= ceil(2 / 3 * self.table_dimension)
            or self.black_stacks >= ceil(2 / 3 * self.table_dimension)
        ):
            return True

    def play_game(self):
        move = self.get_valid_move()
        # play rest of the game
