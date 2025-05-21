

import pygame

from src.hex_grid.hex_grid import get_hex_grid_center_cords, draw_hex_grid

pygame.init()
WIDTH, HEIGHT = 1600, 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)
running = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Boilerplate")

hex_grid = get_hex_grid_center_cords(16, 9)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fps = str(int(clock.get_fps()))
    fps_text = font.render(f"fps: {fps}", True, (255, 255, 255))

    screen.fill(BLACK)
    draw_hex_grid(screen, WHITE, hex_grid, 40, 30)

    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)


