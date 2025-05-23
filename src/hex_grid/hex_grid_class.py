import numpy as np
import pygame


class HexGrid:
    def __init__(self, width: int, height: int, color):
        self.width = width
        self.height = height
        self.color = color
        self.center_cords = None
        self.lines_cords = None

        self.get_center_cords()
        self.get_lines_cords()
        # self.add_perspective_vectorized()

    def get_center_cords(self):    # made by GROK
        height, width = self.height, self.width
        rows = np.arange(height, dtype=np.int_).reshape(height, 1)
        cols = np.arange(width, dtype=np.int_)
        x = 1 + rows % 2 + cols * 2
        y = 2 + 3 * rows
        y = np.broadcast_to(y, shape=(height, width))   # Broadcast to (height, width)
        self.center_cords = np.stack(arrays=(x, y), axis=2)
        self.center_cords.shape = (height * width, 2)

    def get_lines_cords(self):  # shape = (height*width, 4, 2)
        x = self.center_cords[:, 0]
        y = self.center_cords[:, 1]
        self.lines_cords = np.stack([
            np.column_stack((x-1, y+1)),
            np.column_stack((x-1, y-1)),
            np.column_stack((x, y-2)),
            np.column_stack((x+1, y-1))
        ], axis=1)

    def scale_and_scroll(self, scroll, x_scale=40, y_scale=30):
        new_x = self.lines_cords[..., 0] * x_scale - scroll.x
        new_y = self.lines_cords[..., 1] * y_scale - scroll.y
        return np.stack((new_x, new_y), axis=-1)

    def add_perspective_vectorized(self, scroll, x_scale=10, y_scale=10,
                                   x_center=800, h=0.05, y_shift=0, e=1.2, surface_height=900):
        points = self.scale_and_scroll(scroll, x_scale, y_scale)
        h = scroll.z/10
        scaling_factor = 1 + h - h * 2 * points[..., 1] / surface_height
        # scaling_factor = 1 - h + h * 2 * points[..., 1] / surface_height

        new_x = x_center + (points[..., 0] - x_center) / scaling_factor
        # new_y = (y_shift + e * points[..., 1]) / scaling_factor
        new_y = 900 - (900 - points[..., 1]) / scaling_factor
        return np.stack((new_x, new_y), axis=-1)

    def draw(self, surface, scroll, x_scale=10, y_scale=10):
        surface_height = surface.get_size()[1]
        final_line_cords = self.add_perspective_vectorized(scroll, x_scale, y_scale, surface_height=surface_height)
        for line_cords in final_line_cords:
            pygame.draw.aalines(surface, self.color, False, line_cords)


if __name__ == "__main__":
    hex_grid1 = HexGrid(10, 10, (0, 0, 0))


""" ### COMMENT BLOCK





"""


class OldHexGrid:
    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        self.color = color
        self.center_cords = None
        self.lines_cords = None

    def get_hex_grid_center_cords(self):
        self.center_cords = np.zeros((self.height, self.width, 2), dtype=np.int_)
        for y in range(self.height):
            for x in range(self.width):
                self.center_cords[y, x] = (1 + y % 2 + x*2, 2+3*y)
        self.center_cords.shape = (self.height*self.width, 2)

    @staticmethod
    def get_line_cords(cord):
        x, y = cord
        return np.array([(x-1, y+1), (x-1, y-1), (x, y-2), (x+1, y-1)])

    def get_all_hex_line_cords(self):
        self.lines_cords = np.apply_along_axis(self.get_line_cords, 1, self.center_cords)

    @staticmethod
    def add_perspective(cord, x_center=800, h=0.0005, y_shift=0, e=1):
        x, y = cord
        x_perspective = x_center + (x - x_center) / (h * y + 1)
        y_perspective = (y_shift + e * y) / (h * y + 1)
        return np.array([x_perspective, y_perspective])

    def add_perspective_along_axis(self):
        return np.apply_along_axis(self.add_perspective, 2, self.lines_cords)





