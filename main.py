import game


def table_dimension_input():
    table_dimension = input("Enter the table dimension: ")
    if table_dimension.isdigit():
        table_dimension = int(table_dimension)
        if table_dimension % 2 == 0 and table_dimension > 0:
            return table_dimension
        else:
            print("Please enter a positive even number.")
            table_dimension_input()


if __name__ == "__main__":
    human_first = "Y"  #input("Will human play first? (Y/N):")
    table_dimension = 8  # table_dimension_input()
    byte_game = game.Game(human_first, table_dimension)
    byte_game.play_game()
