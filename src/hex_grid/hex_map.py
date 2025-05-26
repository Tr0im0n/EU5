import numpy as np
import pygame


class HexMap:
    def __init__(self, width: int= 64, height: int= 64):
        self.width = width
        self.height = height

        self.col_n = np.arange(self.width, dtype=np.int16)
        self.row_n = np.arange(self.height, dtype=np.int16).reshape(self.height, 1)

        self.grid_cords = None
        self.center_cords = None

    def get_grid_cords(self):
        x = np.broadcast_to(self.col_n, shape=(self.height, self.width))
        y = np.broadcast_to(self.row_n, shape=(self.height, self.width))
        self.grid_cords = np.stack(arrays=(x, y), axis=2)

    def get_center_cords(self):
        x = 1 + self.row_n * 2 + self.col_n % 2
        y = 2 + 3 * self.col_n
        y = np.broadcast_to(y, shape=(self.height, self.width))
        self.center_cords = np.stack(arrays=(x, y), axis=2)

    def make_ocean(self):
        return np.zeros((self.height, self.height), dtype=np.int8) - 2

    @staticmethod
    def make_color_array(array):
        ans = np.zeros((array.shap[0], 3), dtype=np.float32)
        for i, key in enumerate(array):
            ans[i] = color_map_normalized[key]

        return ans

    def make_random_tiles(self):













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





