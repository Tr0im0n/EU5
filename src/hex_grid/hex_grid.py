
import numpy as np
import pygame


def get_hex_grid_center_cords_old(width, height):
    ans = np.zeros((height, width, 2), dtype=np.int_)
    for y in range(height):
        for x in range(width):
            ans[y, x] = (1 + y % 2 + x*2, 2+3*y)
    ans.shape = (height*width, 2)
    return ans


def get_hex_grid_center_cords(width, height):                   # made by GROK
    rows = np.arange(height, dtype=np.int_).reshape(height, 1)  # Shape (height, 1)
    cols = np.arange(width, dtype=np.int_)                      # Shape (width,)
    x = 1 + rows % 2 + cols * 2                                 # Shape (height, width)
    y = 2 + 3 * rows                                            # Shape (height, width)
    y = np.broadcast_to(y, shape=(height, width))               # Broadcast to (height, width)
    ans = np.stack(arrays=(x, y), axis=2)                       # Shape (height, width, 2)
    ans.shape = (height * width, 2)                             # Reshape to (height*width, 2)
    return ans


def get_hex_line_cords(cord):
    x, y = cord
    return np.array([(x-1, y+1), (x-1, y-1), (x, y-2), (x+1, y-1)])


def get_all_hex_line_cords(hex_grid):
    return np.apply_along_axis(get_hex_line_cords, 1, hex_grid)


def get_all_hex_line_cords_stack(hex_grid):
    x = hex_grid[:, 0]
    y = hex_grid[:, 1]
    return np.stack([
        np.column_stack((x-1, y+1)),
        np.column_stack((x-1, y-1)),
        np.column_stack((x, y-2)),
        np.column_stack((x+1, y-1))
    ], axis=1)


def add_perspective(cord, x_center=800, h=0.0005, y_shift=0, e=1):
    x, y = cord
    # x_perspective = x_center + (x - x_center) / (h * y + 1)
    # y_perspective = (y_shift + e * y) / (h * y + 1)
    x_perspective = x_center + (x - x_center) / (h * y + 1)
    y_perspective = (y_shift + e * y) / (h * y + 1)
    return np.array([x_perspective, y_perspective])


def add_perspective_along_axis(points):
    return np.apply_along_axis(add_perspective, 2, points)


def add_perspective_vectorized(points, x_center=800, h=0.0005, y_shift=0, e=1):
    return np.stack((x_center + (points[..., 0] - x_center) / (h * points[..., 1] + 1),
                     (y_shift + e * points[..., 1]) / (h * points[..., 1] + 1)),
                    axis=-1)


def draw_hex_grid(surface, color, hex_grid, x_interval_length=10, y_interval_length=10):
    transform_matrix = np.array( (x_interval_length, y_interval_length) )
    # hex_line_cords = get_all_hex_line_cords(hex_grid)

    for hex_center_cord in hex_grid:
        points = get_hex_line_cords(hex_center_cord) * transform_matrix
        perspective_points = np.apply_along_axis(add_perspective, 1, points)
        pygame.draw.lines(surface, color, False, perspective_points)


if __name__ == "__main__":
    grid = get_hex_grid_center_cords(6, 6)
    print(grid)
    first_hex_lines = get_hex_line_cords(1, 2)
    print(first_hex_lines)









