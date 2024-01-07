from src.get_levels import Game


def main():
    """
    Main function of the game which contains the loop of the game.
    Creates instance of Game and calls step method or start screen method.
    """
    game = Game()
    while game.running:
        if game.status == 0:
            game.start_screen()
        elif game.status == 1:
            game.step()
        else:
            game.end_screen()


if __name__ == '__main__':
    main()
