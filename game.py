from get_levels import Game


def main():
    game = Game()
    while game.running:
        game.step()


if __name__ == '__main__':
    main()
