import pygame


def get_screen_size():
    """
    Calculates display width and height so it is in 16/9 ratio
    and the factor by which it was resized compared to 1080p resolution.
    """
    screen = pygame.display.Info()
    width = screen.current_w
    height = screen.current_h
    if width / height > 16 / 9:
        factor = height / 1080
        return (1920 * factor, height, factor)
    else:
        factor = width / 1920
        return (width, 1080 * factor, factor)


pygame.init()
screen = get_screen_size()
SCREEN_WIDTH = 1913
SCREEN_HEIGHT = 1050
DISPLAY_WIDTH = int(screen[0]) - 7
DISPLAY_HEIGHT = int(screen[1]) - 30
screen_factor = screen[2]
FPS = 30
gravity = (0, -500)
bird_radius = 20
bird_position = (220, 200 + bird_radius)
floor_height = 200
aiming_range = 200
