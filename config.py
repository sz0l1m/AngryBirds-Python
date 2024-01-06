import pygame


def get_screen_size():
    screen = pygame.display.Info()
    width = screen.current_w
    height = screen.current_h
    print(width / height)
    if width / height > 16 / 9:
        return (1920 * (height / 1080), height)
    else:
        return (width, 1080 * (width / 1920))


pygame.init()
screen = get_screen_size()
SCREEN_WIDTH = int(screen[0]) - 7
SCREEN_HEIGHT = int(screen[1]) - 30
FPS = 30
gravity = (0, -500)
bird_radius = 20
bird_position = (220, 200 + bird_radius)
floor_height = 200
aiming_range = 200
