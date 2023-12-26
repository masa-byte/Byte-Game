def translate_state_to_facts(game, color, move):
    facts = set()
    if color == "W":
        if game.white_stacks > game.black_stacks:
            facts.add(1)
        elif game.white_stacks < game.black_stacks:
            facts.add(2)
    elif color == "B":
        if game.black_stacks > game.white_stacks:
            facts.add(1)
        elif game.black_stacks < game.white_stacks:
            facts.add(2)
    if game.white_stacks == game.black_stacks:
        facts.add(3)

    current_stack, stack_i, stack_j = game.game_table.get_destination_stack(
        move.i, move.j, move.direction
    )

    if current_stack.get_color_of_top_coin() == color:
        facts.add(4)
    else:
        facts.add(5)

    facts.add(6)

    vicinity_stacks = game.game_table.get_vicinity_stacks(stack_i, stack_j)

    number_of_coins_in_curent_stack = current_stack.get_number_of_coins()
    number_of_computer_coins_in_vicinity_stacks = 0
    number_of_human_coins_in_vicinity_stacks = 0

    for stack in vicinity_stacks:
        if stack.get_color_of_top_coin() == color:
            facts.add(7)
        else:
            facts.add(8)
        number_of_computer_coins_in_vicinity_stacks += stack.get_number_of__color_coins(color)
        number_of_human_coins_in_vicinity_stacks += stack.get_number_of_color_coins("W" if color == "B" else "B")

    if number_of_coins_in_curent_stack + number_of_computer_coins_in_vicinity_stacks == 8:
        facts.add(9)
    elif number_of_coins_in_curent_stack + number_of_computer_coins_in_vicinity_stacks < 8:
        facts.add(10)
    else:
        facts.add(11)

    if number_of_coins_in_curent_stack + number_of_human_coins_in_vicinity_stacks == 8:
        facts.add(12)
    elif number_of_coins_in_curent_stack + number_of_human_coins_in_vicinity_stacks < 8:
        facts.add(13)
    else:
        facts.add(14)

    return facts