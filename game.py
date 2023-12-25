import table
import move
from math import floor
from copy import deepcopy
import random

class Game:
    def __init__(self, human_first, table_dimension):
        self.human_first = True if human_first == "Y" else False
        self.table_dimension = table_dimension
        self.number_of_stacks = int((self.table_dimension - 2) * self.table_dimension / 2) / 8
        self.game_table = table.Table(table_dimension)
        self.game_table.print_table()
        print('////////////////////////////////////////////////////////')

        self.player_color = 0

        self.white_stacks = 0
        self.black_stacks = 0

    def get_human_valid_and_allowed_move(self, color):
        while True:
            print("Enter i, j, coin_position_in_stack, direction")
            print("Valid directions: TL, TR, BL, BR")
            splited_input = input(color + " Enter move: ").split()
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
                    player_move = move.Move(int(i), int(j), int(coin_position_in_stack), direction, color)
                    if self.game_table.is_move_valid(player_move):
                        if self.game_table.is_move_allowed(player_move):
                            return player_move
                        else:
                            print("Move not allowed")
                    else: 
                        print("Move not valid")

    def get_computer_valid_and_allowed_move(self, color):
        # TO DO: U 3. fazi izmeniti da se uzima najbolji potez
        best_move = self.minimax(1, True, color, None)
        return best_move[2]

    def get_valid_and_allowed_move(self, color):
        if self.human_first and color == 'W':
            return self.get_human_valid_and_allowed_move(color)
        elif not self.human_first and color == 'B':
            return self.get_human_valid_and_allowed_move(color)
        else:
            return self.get_computer_valid_and_allowed_move(color)

    def is_game_over(self):
        if (
            self.game_table.is_table_empty()
            or self.white_stacks >= floor(self.number_of_stacks / 2 + 1)
            or self.black_stacks >= floor(self.number_of_stacks / 2 + 1)
        ):
            return True
        return False

    def get_next_color(self):
        color = 'W' if self.player_color == 0 else 'B'
        self.player_color += 1
        self.player_color %= 2
        return color

    def play_game(self):
        while True:
            color = self.get_next_color()
            move = self.get_valid_and_allowed_move(color)
            result = self.game_table.play_move(move)
            if result != None:
                if result == 'B':
                    self.black_stacks += 1
                    if self.is_game_over():
                        print("Black wins")
                        break
                elif result == 'W':
                    self.white_stacks += 1
                    if self.is_game_over():
                        print("White wins")
                        break
            self.game_table.print_table()
            print('////////////////////////////////////////////////////////')

    def evaluate_state(self):
        return random.uniform(-1, 1)

    def max_state(self, lsv):
        return max(lsv, key=lambda x: x[1])
    
    def min_state(self, lsv):
        return min(lsv, key=lambda x: x[1])
    
    def minimax(self, depth, my_move, color, move):
        list_of_moves = self.game_table.get_all_allowed_moves(color)
        list_of_games_and_moves = []
        for possible_move in list_of_moves:
            game = deepcopy(self)
            game.game_table.play_move(possible_move)
            list_of_games_and_moves.append((game, possible_move))
        if depth == 0 or list_of_moves is None:
            return(self, self.evaluate_state(), move)
        lsv = [game_and_move[0].minimax(depth - 1, not my_move, "B" if color == "W" else "W", game_and_move[1]) for game_and_move in list_of_games_and_moves]
        if my_move:
            return self.max_state(lsv)
        else:
            return self.min_state(lsv)
        
