import pygame
pygame.init()
pygame_info = pygame.display.Info()
SCREEN_WIDTH = pygame_info.current_w - 7
SCREEN_HEIGHT = pygame_info.current_h - 30
FPS = 30
gravity = (0, -500)
bird_radius = 20
bird_position = (220, 200 + bird_radius)
floor_height = 200
aiming_range = 200
