
import numpy as np
import pygame


def get_hex_grid_center_cords(width, height):
    n_hexes = width*height
    ans = np.zeros((n_hexes, 2), dtype=np.int_)
    x, y = 0, 0
    for i in range(n_hexes):
        ans[i] = (1 + y % 2 + x*2, 2+3*y)
        x += 1
        if x == width:
            x = 0
            y += 1
    return ans


def get_hex_line_cords(x, y):
    return np.array([(x-1, y+1), (x-1, y-1), (x, y-2), (x+1, y-1)])


def draw_hex_grid(surface, color, hex_grid, x_interval_length=10, y_interval_length=10):
    transform_matrix = np.array( (x_interval_length, y_interval_length) )
    for hex_center_cord in hex_grid:
        points = get_hex_line_cords(*hex_center_cord) * transform_matrix
        pygame.draw.lines(surface, color, False, points)


if __name__ == "__main__":
    grid = get_hex_grid_center_cords(6, 6)
    print(grid)
    first_hex_lines = get_hex_line_cords(1, 2)
    print(first_hex_lines)








