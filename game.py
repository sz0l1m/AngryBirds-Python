from src.get_levels import Game


def main():
    """
    Main function of the game which contains the loop of the game.
    Creates instance of Game and calls step method or start screen method.
    """
    game = Game()
    while game.running:
        if game.start:
            game.step()
        else:
            game.start_screen()


if __name__ == '__main__':
    main()
