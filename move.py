allowed_directions = ["TL", "TR", "BL", "BR"]

class Move:
    def __init__(self, field: tuple, coin_position_in_stack, direction):
        self.field = field
        self.coin_position_in_stack = coin_position_in_stack
        self.direction = direction
        # color of coin, depends on who plays
        self.coint_color = None

    def is_direction_valid(self):
        return True if self.direction in allowed_directions else False
        

    