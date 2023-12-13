import directions

class Move:
    def __init__(self, i, j, coin_position_in_stack, direction, color):
        self.i = i
        self.j = j
        self.coin_position_in_stack = coin_position_in_stack
        self.direction = direction
        self.coin_color = color

    def is_direction_valid(self):
        return True if self.direction in map(lambda en: en.value, directions.Direction) else False

    def __str__(self):
        return f"{self.i} {self.j} {self.coin_position_in_stack} {self.direction}"    

    