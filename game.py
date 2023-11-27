import table
import move


class Game:
    def __init__(self, human_first, table_dimension):
        self.human_first = human_first
        self.human_first = True if human_first == "1" else False
        self.table_dimension = table_dimension
        self.game_table = table.Table(table_dimension)
        self.game_table.print_table()

    def get_valid_move(self):
        while True:
            print("Enter i, j, coin_position_in_stack, direction")
            i, j, coin_position_in_stack, direction = [
                x for x in input("Enter move: ").split()
            ]
            player_move = move.Move((i, j), coin_position_in_stack, direction)
            outcome = self.game_table.is_move_valid(player_move)
            if outcome:
                return player_move
            
    def is_game_over(self):
        if self.game_table.is_table_empty():
            return True

    def play_game(self):
        move = self.get_valid_move()
        # play rest of the game
