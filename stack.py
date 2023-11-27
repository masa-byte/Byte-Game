def first_next_full_root_square(number):
    for i in range(1, number):
        if i * i > number:
            return i
    return 0


class WhiteField:
    def __init__(self, n):
        self.num_print_el = first_next_full_root_square(n)

    def print_field(self):
        matrix = [
            [" " for _ in range(self.num_print_el)] for _ in range(self.num_print_el)
        ]
        return matrix

    def is_empty(self):
        return True


class Stack:
    def __init__(self, n):
        self.capacity = n
        self.elements = []
        self.num_print_el = first_next_full_root_square(n)

    def push(self, el):
        if self.capacity == len(self.elements):
            raise IndexError("Stack is full")
        self.elements.append(el)

    def print_field(self):
        matrix = [
            [
                "."
                if i * self.num_print_el + j >= len(self.elements)
                else self.elements[i * self.num_print_el + j]
                for j in range(self.num_print_el)
            ]
            for i in range(self.num_print_el)
        ]
        return matrix
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def does_coin_exist_at_position(self, coin_position_in_stack):
        return coin_position_in_stack < len(self.elements)
