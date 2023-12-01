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

    def push(self, el):
        if self.capacity == len(self.elements):
            raise IndexError("Black field is full")
        self.elements.append(el)

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
    
    def does_coin_exist_at_position(self, coin_position_in_stack, coin_color):
        return (
            False
            if coin_position_in_stack >= len(self.elements)
            else self.elements[coin_position_in_stack] == coin_color
        )
