

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from utils.import_asset import import_texture


sqrt3 = np.sqrt(3)
width = 18 # normal 37
height = 21 # normal 42
file_name = "seed_05.png"

marsh = 60
grassland = 63
hills = 148
mountain = 185

# first convert to hex tiles
# then to topography type

def get_hex_heightmap():
    texture = import_texture(file_name, "GRAY")
    heightmap = np.array(texture, dtype=np.uint8)
    hex_heightmap = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            tex_x = 1 + (x * 2 + y%2) * sqrt3 * 2 # normal without the * 2
            tex_y = 2 + 3 * y * 2 # normal without the * 2
            floor_x = np.floor(tex_x, casting='unsafe', dtype=np.uint8)
            ceil_x = np.ceil(tex_x, casting='unsafe', dtype=np.uint8)
            fract_x = tex_x%1
            left = heightmap[tex_y, floor_x]
            right = heightmap[tex_y, ceil_x]
            interpolated = fract_x * right + (1 - fract_x) * left
            hex_heightmap[y, x] = interpolated
    return hex_heightmap

# finished converting it to my hex coordinates
# could change the dimensions on a next run

def get_topography_type_old(hex_heightmap):
    topography_type = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            map_height = hex_heightmap[y, x]
            if map_height < 60:
                ans = 0
            elif map_height < 102:
                ans = 1
            elif map_height < 153:
                ans = 2
            elif map_height < 204:
                ans = 3
            else:
                ans = 4
            print(map_height, ans)
            topography_type[y, x] = ans
    return topography_type


def get_topography_type(matrix):
    conditions = [
        matrix < marsh,
        (matrix >= marsh) & (matrix < grassland),
        (matrix >= grassland) & (matrix < hills),
        (matrix >= hills) & (matrix < mountain),
        matrix >= mountain
    ]
    # choices = [0, 1, 2, 3, 4]
    choices = [5, 0, 1, 2, 4]
    return np.select(conditions, choices, default=0).astype(np.uint8)


def main():
    hex_heightmap = get_hex_heightmap()
    topography_type = get_topography_type(hex_heightmap)
    topography_type[0, 0] = 5
    fig, (ax1, ax2) = plt.subplots(1, 2)
    im1 = ax1.imshow(hex_heightmap, cmap='terrain', origin='lower')
    fig.colorbar(im1, ax=ax1, label="Height")
    im2 = ax2.imshow(topography_type, cmap='terrain', origin='lower')
    # im2 = ax2.imshow(topography_type_2, cmap='terrain', origin='lower')
    fig.colorbar(im2, ax=ax2, label="Height")
    plt.show()

    img_grayscale = Image.fromarray(topography_type, mode='L')
    img_grayscale.save(f"topography_05_small.png")

if __name__ == "__main__":
    main()

