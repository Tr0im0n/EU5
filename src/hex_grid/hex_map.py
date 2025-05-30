import random

import numpy as np
import pygame

from src.random.dijkstra import dijkstra_2, dijkstra_3


class HexMap:
    def __init__(self, width: int= 64, height: int= 64):
        self.width = width
        self.height = height

        self.col_n = np.arange(self.width, dtype=np.int16)
        self.row_n = np.arange(self.height, dtype=np.int16).reshape(self.height, 1)

        self.corner_offsets = np.array([0, -2, -1, -1, -1, 1, 0, 2, 1, 1, 1, -1], dtype=np.float32)

        self.grid_cords = None
        self.center_cords = None
        self.adjacent_nodes = None
        self.travel_cost = None
        self.distances = None

        self.get_center_cords()
        self.get_adjacent_nodes_comprehension()
        self.make_random_tiles()
        self.get_distances()
        print(self.distances.shape)


    def get_grid_cords(self):
        x = np.broadcast_to(self.col_n, shape=(self.height, self.width))
        y = np.broadcast_to(self.row_n, shape=(self.height, self.width))
        self.grid_cords = np.stack(arrays=(x, y), axis=2)

    def get_center_cords(self):
        x = 1 + self.col_n * 2 + self.row_n % 2
        y = 2 + 3 * self.row_n
        y = np.broadcast_to(y, shape=(self.height, self.width))
        self.center_cords = np.stack(arrays=(x, y), axis=2)

    def make_random_tiles(self):
        random.seed(25)
        self.travel_cost = np.random.randint(10, 41, size=(self.height, self.width))

    def get_adjacent_nodes(self):
        ans = {}
        for y in self.row_n[1:-1]:
            for x in self.col_n[1:-1]:
                x_offset = x+y%2
                ans[(y, x)] = {
                    (y, x-1), (y, x+1),
                    (y-1, x_offset-1), (y-1, x_offset),
                    (y+1, x_offset-1), (y+1, x_offset)}
        self.adjacent_nodes = ans

    def get_adjacent_nodes_comprehension(self):
        self.adjacent_nodes = {(y, x): [
                (y, x - 1),  # Direct left
                (y, x + 1),  # Direct right
                (y - 1, x + (y % 2) - 1), # Upper-left relative to x_offset
                (y - 1, x + (y % 2)),     # Upper-right relative to x_offset
                (y + 1, x + (y % 2) - 1), # Lower-left relative to x_offset
                (y + 1, x + (y % 2))]     # Lower-right relative to x_offset
            for y in range(1, self.height-1)
            for x in range(1, self.width-1)}

    def get_adjacent_nodes_array(self):
        y = self.row_n
        x = self.col_n
        ans = [
            y, x - 1,  # Direct left 01
            x + 1,  # Direct right y, 02
            y - 1, x + y % 2 - 1,  # Upper-left relative to x_offset 34
            x + y % 2,  # Upper-right relative to x_offset y - 1, 35
            y + 1  # Lower-left relative to x_offset , x + y % 2 - 1, 64
            ]  # Lower-right relative to x_offset y + 1, x + y % 2 65
        indices = (0, 1, 0, 2, 3, 4, 3, 5, 6, 4, 6, 5)
        self.adjacent_nodes = np.stack(ans[indices], axis=2)

    def get_distances(self):
        starting_node = (10, 10)
        distances = dijkstra_3(self.adjacent_nodes, starting_node, self.travel_cost)
        self.distances = np.zeros((self.height, self.width), dtype=np.float32)
        for i, j in distances.items():
            self.distances[*i] = j

    @staticmethod
    def make_color_array(array):
        ans = np.zeros((array.shap[0], 3), dtype=np.float32)
        for i, key in enumerate(array):
            ans[i] = color_map_normalized[key]

        return ans

    def make_ocean(self):
        return np.zeros((self.height, self.height), dtype=np.int8) - 2

    @staticmethod
    def get_single_adjacent(y, x):
        x_offset = x+y%2
        return {(y, x-1): 1,
               (y, x+1): 1,
               (y-1, x_offset-1): 1,
               (y-1, x_offset): 1,
               (y+1, x_offset-1): 1,
               (y+1, x_offset): 1}







color_map_normalized = {
    4: [0.54509804, 0.27058824, 0.0745098],  # Mountains (SaddleBrown)
    3: [0.72156863, 0.5254902, 0.04313725],  # Plateau (DarkGoldenrod)
    2: [0.59607843, 0.98431373, 0.59607843],  # Hills (PaleGreen)
    1: [0.23529412, 0.70196078, 0.44313725],  # Flat (MediumSeaGreen)
    0: [0.54509804, 0.41176471, 0.07843137],  # Marsh (DarkKhaki)
    -1: [0.39215686, 0.58431373, 0.92941176],  # Coastal Water (CornflowerBlue)
    -2: [0.09803922, 0.09803922, 0.43921569]  # Ocean (MidnightBlue)
}


"""

4 mountains
3 plateau
2 hills
1 flat
0 marsh
-1 coastal water
-2 ocean

"""





