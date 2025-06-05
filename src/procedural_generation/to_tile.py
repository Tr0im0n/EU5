

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from utils.import_asset import import_texture


sqrt3 = np.sqrt(3)
width = 37
height = 42



file_name = "seed_05.png"
texture = import_texture(file_name, "GRAY")
heightmap = np.array(texture, dtype=np.uint8)

# first convert to hex tiles
# then to topography type

hex_heightmap = np.zeros((42, 37), dtype=np.uint8)
for y in range(height):
    for x in range(width):
        tex_x = (1 + x * 2 + y%2) * sqrt3
        tex_y = 2 + 3 * y
        floor_x = np.floor(tex_x, casting='unsafe', dtype=np.uint8)
        ceil_x = np.ceil(tex_x, casting='unsafe', dtype=np.uint8)
        fract_x = tex_x%1
        left = heightmap[tex_y, floor_x]
        right = heightmap[tex_y, ceil_x]
        interpolated = fract_x * right + (1 - fract_x) * left
        hex_heightmap[y, x] = interpolated

# finished converting it to my hex coordinates
# could change the dimensions on a next run

# topography_type = np.zeros((42, 37), dtype=np.uint8)
# for y in range(height):
#     for x in range(width):
#         ans = 0
#         map_height = heightmap[y, x]
#         if map_height < 51:
#             ans = 5
#         elif map_height < 102:
#             ans = 0
#         elif map_height < 153:
#             ans = 1
#         elif map_height < 204:
#             ans = 2
#         # elif map_height < 0.2:
#         #     ans = 3
#         else:
#             ans = 4
#         topography_type[y, x] = ans

# topography_type_2 = np.zeros((42, 37), dtype=np.uint8)

topography_type_2 = hex_heightmap/51

fig, (ax1, ax2) = plt.subplots(1, 2)

im1 = ax1.imshow(hex_heightmap, cmap='terrain', origin='lower')
fig.colorbar(im1, ax=ax1, label="Height")
im2 = ax2.imshow(topography_type_2, cmap='terrain', origin='lower')
fig.colorbar(im2, ax=ax2, label="Height")
plt.show()

# img_grayscale = Image.fromarray(topography_type, mode='L')
# img_grayscale.save(f"topography_05.png")

