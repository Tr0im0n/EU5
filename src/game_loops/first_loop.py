

import pygame

from src.game_loops.scroll import Scroll
from src.hex_grid.hex_grid import get_hex_grid_center_cords, draw_hex_grid
from src.hex_grid.hex_grid_class import HexGrid

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
dragging, last_pos = 0, 0

scroll = Scroll(x_ub=800, y_ub=450)
hex_grid2 = HexGrid(16, 9, WHITE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                dragging = True
                last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                dragging = False
                last_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging and last_pos:
                current_pos = event.pos
                dx = current_pos[0] - last_pos[0]
                dy = current_pos[1] - last_pos[1]
                scroll.x -= dx  # Move x opposite to mouse movement
                scroll.y -= dy  # Move y opposite to mouse movement
                last_pos = current_pos
        elif event.type == pygame.MOUSEWHEEL:
            scroll.z += event.y * 0.5  # Scroll up (1) or down (-1), scaled by 0.5

    fps = str(int(clock.get_fps()))
    fps_text = font.render(f"fps: {fps}", True, WHITE)

    screen.fill(BLACK)
    hex_grid2.draw(screen, scroll, 40, 30)

    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)




pygame.quit()

