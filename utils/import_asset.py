import os

import numpy as np
from PIL import Image
import pandas as pd


def import_shader(file_name):

    current_script_path = os.path.abspath(__file__)
    root_directory = os.path.join(current_script_path, "..", "..")

    with open(os.path.join(root_directory, 'assets', 'shaders', file_name), 'r') as file:
        ans = file.read()
    return ans


def import_texture(file_name, color_scale="RGBA"):

    current_script_path = os.path.abspath(__file__)
    root_directory = os.path.join(current_script_path, "..", "..")

    if color_scale == "GRAY":
        return Image.open(os.path.join(root_directory, 'assets', 'textures', file_name))

    return Image.open(os.path.join(root_directory, 'assets', 'textures', file_name)).convert('RGBA')


def import_csv(file_name):

    current_script_path = os.path.abspath(__file__)
    root_directory = os.path.join(current_script_path, "..", "..")

    df = pd.read_csv(os.path.join(root_directory, 'assets', 'hex_grid', file_name))

    tile_type_list = df["tile_type"].to_list()
    ans = np.zeros((400, 3), np.float32)
    for i, tile_type_str in enumerate(tile_type_list):
        ans[i] = TileColors.get_color(tile_type_str)[:3]

    return ans













class TileColors:
    GRASSLAND = (0.486, 0.733, 0.333, 1.0)
    FARMLAND  = (0.745, 0.706, 0.431, 1.0)
    WOODS     = (0.314, 0.510, 0.314, 1.0)
    FOREST    = (0.157, 0.392, 0.157, 1.0)
    HILL      = (0.588, 0.471, 0.314, 1.0)
    MOUNTAIN  = (0.471, 0.490, 0.510, 1.0)
    COASTAL_WATER = (0.510, 0.784, 0.902, 1.0)
    OCEAN         = (0.235, 0.471, 0.706, 1.0)

    @classmethod
    def get_color(cls, tile_type: str) -> tuple[float, float, float, float] | None:
        return getattr(cls, tile_type.upper(), None)


