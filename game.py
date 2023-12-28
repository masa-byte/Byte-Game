import table
import move
from math import floor
from copy import deepcopy
import heuristics as h
import sys

search_depth = 3


class Game:
    def __init__(self, human_first, table_dimension):
        self.human_first = True if human_first == "Y" else False
        self.table_dimension = table_dimension
        self.number_of_stacks = (
            int((self.table_dimension - 2) * self.table_dimension / 2) / 8
        )
        self.game_table = table.Table(table_dimension)
        self.game_table.print_table()
        print("////////////////////////////////////////////////////////")

        self.player_color = 0

        self.white_stacks = 0
        self.black_stacks = 0

        self.last_move = None

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
                    player_move = move.Move(
                        int(i), int(j), int(coin_position_in_stack), direction, color
                    )
                    if self.game_table.is_move_valid(player_move):
                        if self.game_table.is_move_allowed(player_move):
                            return player_move
                        else:
                            print("Move not allowed")
                    else:
                        print("Move not valid")

    def get_computer_valid_and_allowed_move(self, color):
        best_move = self.minimax_alpha_beta(search_depth, True, color)
        print(best_move[0].last_move)
        return best_move[0].last_move

    def get_valid_and_allowed_move(self, color):
        if self.human_first and color == "W":
            return self.get_human_valid_and_allowed_move(color)
        elif not self.human_first and color == "B":
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
        color = "W" if self.player_color == 0 else "B"
        self.player_color += 1
        self.player_color %= 2
        return color

    def play_game(self):
        while True:
            color = self.get_next_color()
            possible_moves = self.game_table.get_all_allowed_moves(color)
            if len(possible_moves) != 0:
                move = self.get_valid_and_allowed_move(color)
                result = self.game_table.play_move(move)
                self.last_move = move
                if result is not None:
                    if result == "B":
                        self.black_stacks += 1
                        print("Black got a stack")
                        if self.is_game_over():
                            print("Black wins")
                            break
                    elif result == "W":
                        self.white_stacks += 1
                        print("White got a stack")
                        if self.is_game_over():
                            print("White wins")
                            break
            else:
                print("No moves for " + color)
            self.game_table.print_table()
            print("////////////////////////////////////////////////////////")

    ## alpha beta cutoff minimax

    def evaluate_state(self, color, move):
        return h.evaluate_state(self, color, move)

    def max_value(self, depth, alpha, beta, color, last_move):
        list_of_moves = self.game_table.get_all_allowed_moves(color)
        if depth == 0 or len(list_of_moves) == 0 or list_of_moves is None:
            return (self, self.evaluate_state(color, self.last_move))
        list_of_games = []
        for possible_move in list_of_moves:
            game = deepcopy(self)
            game.game_table.play_move(possible_move)
            game.last_move = last_move
            list_of_games.append(game)

        for game in list_of_games:
            alpha = max(
                alpha,
                game.min_value(
                    depth - 1, alpha, beta, "W" if color == "B" else "B", last_move
                ),
                key=lambda x: x[1],
            )
            if alpha[1] >= beta[1]:
                return beta
        return alpha

    def min_value(self, depth, alpha, beta, color, last_move):
        list_of_moves = self.game_table.get_all_allowed_moves(color)
        if depth == 0 or len(list_of_moves) == 0 or list_of_moves is None:
            return (self, self.evaluate_state(color, self.last_move))
        list_of_games = []
        for possible_move in list_of_moves:
            game = deepcopy(self)
            game.game_table.play_move(possible_move)
            game.last_move = last_move
            list_of_games.append(game)

        for game in list_of_games:
            beta = min(
                beta,
                game.max_value(
                    depth - 1, alpha, beta, "W" if color == "B" else "B", last_move
                ),
                key=lambda x: x[1],
            )
            if alpha[1] >= beta[1]:
                return alpha
        return beta

    def initial_max_value(self, depth, alpha, beta, color):
        list_of_moves = self.game_table.get_all_allowed_moves(color)
        if len(list_of_moves) == 0 or list_of_moves is None:
            return "empty"
        list_of_games = []
        for possible_move in list_of_moves:
            game = deepcopy(self)
            game.game_table.play_move(possible_move)
            game.last_move = possible_move
            list_of_games.append(game)

        for game in list_of_games:
            alpha = max(
                alpha,
                game.min_value(
                    depth - 1, alpha, beta, "W" if color == "B" else "B", game.last_move
                ),
                key=lambda x: x[1],
            )
            if alpha[1] >= beta[1]:
                return beta
        return alpha

    def initial_min_value(self, depth, alpha, beta, color):
        list_of_moves = self.game_table.get_all_allowed_moves(color)
        if list_of_moves is None:
            return "empty"
        list_of_games = []
        for possible_move in list_of_moves:
            game = deepcopy(self)
            game.game_table.play_move(possible_move)
            game.last_move = possible_move
            list_of_games.append(game)

        for game in list_of_games:
            beta = min(
                beta,
                game.max_value(
                    depth - 1, alpha, beta, "W" if color == "B" else "B", game.last_move
                ),
                key=lambda x: x[1],
            )
            if alpha[1] >= beta[1]:
                return alpha
        return beta

    def minimax_alpha_beta(
        self,
        depth,
        my_move,
        color,
        alpha=(None, -sys.maxsize - 1),
        beta=(None, sys.maxsize),
    ):
        if my_move:
            return self.initial_max_value(depth, alpha, beta, color)
        else:
            return self.initial_min_value(depth, alpha, beta, color)
