import game


def table_dimension_input():
    table_dimension = input("Enter the table dimension: ")
    if table_dimension.isdigit():
        table_dimension = int(table_dimension)
        if ((table_dimension - 2) * table_dimension / 2) % 8 == 0 and table_dimension > 0:
            return table_dimension
        else:
            print("Please enter a positive number which follows this rule"
                  "((table_dimension - 2) * table_dimension / 2) % 8 == .")
            print("Example: 8, 10, 16")
            return table_dimension_input()
        
def player_first_input():
    human_first = input("Will human play first? (Y/N): ")
    if human_first == "Y" or human_first == "N" or human_first == "y" or human_first == "n":
        return human_first
    else:
        print("Please enter Y or N.")
        return player_first_input()


if __name__ == "__main__":
    human_first = player_first_input()
    table_dimension = table_dimension_input()
    byte_game = game.Game(human_first, table_dimension)
    byte_game.play_game()
