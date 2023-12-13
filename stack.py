class WhiteField:
    def __init__(self):
        self.num_print_elements = 3

    def print_field(self):
        matrix = [
            [" " for _ in range(self.num_print_elements)]
            for _ in range(self.num_print_elements)
        ]
        return matrix

    def is_empty(self):
        return True


class BlackField:
    def __init__(self):
        self.capacity = 8
        self.num_print_elements = 3
        self.elements = []

    def push(self, elements):
        if self.capacity == len(self.elements):
            raise IndexError("Black field is full")
        self.elements.extend(elements)

    def pop(self, position):
        if len(self.elements) == 0:
            raise IndexError("Black field is empty")
        for_return = self.elements[position:]
        self.elements = self.elements[:position]
        return for_return

    def print_field(self):
        matrix = [
            [
                "."
                if i * self.num_print_elements + j >= len(self.elements)
                else self.elements[i * self.num_print_elements + j]
                for j in range(self.num_print_elements)
            ]
            for i in range(self.num_print_elements)
        ]
        return matrix

    def is_empty(self):
        return len(self.elements) == 0
    
    def does_coin_exist_at_position(self, position, coin_color):
        return (
            False
            if position >= len(self.elements)
            else self.elements[position] == coin_color
        )
    
    def get_number_of_coins(self):
        return len(self.elements)

    def get_number_of_coins_from_position(self, position):
        return len(self.elements) - position

    def get_coins_from_position(self, pos):
        return self.elements[pos:]
