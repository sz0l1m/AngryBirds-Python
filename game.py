from get_levels import Game


def main():
    game = Game()
    while game.running:
        if game.start:
            game.step()
        else:
            game.start_screen()


if __name__ == '__main__':
    main()
