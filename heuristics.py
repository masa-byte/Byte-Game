
facts_wights = {
    4: 0.8,
    5: -0.8,
    6: -0.05,
    7: 0.05,
    8: 0.05,
    9: -0.05,
}


def evaluate_state(game, color, move):
    facts = translate_state_to_facts(game, color, move)
    sum_of_weights = sum([fact[1] for fact in facts])
    return sum_of_weights


def translate_state_to_facts(game, color, move):
    facts = []
    
    current_stack, stack_i, stack_j = game.game_table.get_destination_stack(
        move.i, move.j, move.direction
    )

    if not current_stack.is_empty():
        current_stack_top_coin_color = current_stack.get_color_of_top_coin()
    else:
        current_stack_top_coin_color = None
    number_of_coins_in_curent_stack = current_stack.get_number_of_coins()

    vicinity_stacks = game.game_table.get_vicinity_stacks(stack_i, stack_j)

    for stack in vicinity_stacks:
        color_on_vicinity_stack_top = stack.get_color_of_top_coin()
        number_of_vicinity_stack_coins = stack.get_number_of_coins()

        if number_of_coins_in_curent_stack + number_of_vicinity_stack_coins == 8:
            # vicinity stack on current stack in next round
            if color_on_vicinity_stack_top == color:
                facts.append([4, facts_wights[4]])
            else:
                facts.append([5, facts_wights[5]])
            # current stack on vicinity stack in next round
            if current_stack_top_coin_color == color:
                facts.append([4, facts_wights[4]])
            else:
                facts.append([5, facts_wights[5]])
        elif number_of_coins_in_curent_stack + number_of_vicinity_stack_coins < 8:
            # vicinity stack on current stack in next round
            if color_on_vicinity_stack_top == color:
                facts.append(
                    [
                        6,
                        facts_wights[6]
                        * (
                            number_of_coins_in_curent_stack
                            + number_of_vicinity_stack_coins
                        ),
                    ]
                )
            else:
                facts.append(
                    [
                        7,
                        facts_wights[7]
                        * (
                            number_of_coins_in_curent_stack
                            + number_of_vicinity_stack_coins
                        ),
                    ]
                )
            # current stack on vicinity stack in next round
            if current_stack_top_coin_color == color:
                facts.append(
                    [
                        6,
                        facts_wights[6]
                        * (
                            number_of_coins_in_curent_stack
                            + number_of_vicinity_stack_coins
                        ),
                    ]
                )
            else:
                facts.append(
                    [
                        7,
                        facts_wights[7]
                        * (
                            number_of_coins_in_curent_stack
                            + number_of_vicinity_stack_coins
                        ),
                    ]
                )
        else:
            computer_coins = stack.get_number_of_color_coins(color)
            human_coins = number_of_vicinity_stack_coins - computer_coins
            # vicinity stack on current stack in next round
            if computer_coins > human_coins:
                facts.append(
                    [
                        8,
                        facts_wights[8]
                        * (number_of_coins_in_curent_stack + computer_coins),
                    ]
                )
            else:
                facts.append(
                    [
                        9,
                        facts_wights[9]
                        * (number_of_coins_in_curent_stack + human_coins),
                    ]
                )
            # current stack on vicinity stack in next round
            if computer_coins > human_coins:
                facts.append(
                    [
                        8,
                        facts_wights[8]
                        * (number_of_coins_in_curent_stack + computer_coins),
                    ]
                )
            else:
                facts.append(
                    [
                        9,
                        facts_wights[9]
                        * (number_of_coins_in_curent_stack + human_coins),
                    ]
                )

    return facts
