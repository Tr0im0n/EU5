import moderngl
import numpy as np
import pygame
from pyglm import glm

from src.hex_grid.hex_map import HexMap
from src.random.font_texture import create_font_texture
from src.random.location import get_topography_colors_array
from src.random.model_view_projection import MVP
from src.random.scroll import Scroll
from utils.import_asset import import_shader, import_texture

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
FPS_CAP = 60
# Pygame + ModernGL
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Second Loop")
ctx = moderngl.create_context()
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)
# Global ish variables
running = True
last_pos_for_scroll = None
scroll = Scroll()
mvp = MVP(scroll)
# Shader Programs
flat_color_prog = ctx.program(import_shader("mvp_color_instance.vert"), import_shader("color.frag"))
ui_prog = ctx.program(import_shader("pos_texcoord.vert"), import_shader("texture.frag"))
flat_color_prog['u_mvp_matrix'].write(mvp.update().to_bytes())
new_id_prog = ctx.program(import_shader("tile_type.vert"), import_shader("color.frag"))

###############################################################################################################
#   # Making VAO 's
###############################################################################################################
width = 37
height = 42
n_tiles = width* height # 37*42=1_554

hex_map_1 = HexMap(width, height)
center_cords = hex_map_1.center_cords.astype(np.float32)
center_cords.shape = (n_tiles, 2)
center_cords_vbo = ctx.buffer(center_cords.tobytes())
corner_offsets_vbo = ctx.buffer(hex_map_1.corner_offsets.tobytes())
grid_cords = hex_map_1.grid_cords.astype(np.uint32)
hex_id_vbo = ctx.buffer(grid_cords.tobytes())

# Get color from supposed market access
# distances = hex_map_1.distances
# hex_colors = np.zeros((20, 20, 3), dtype=np.float32)
# for i in (0, 1, 2):
#     mask = distances['start_node'] == i
#     hex_colors[mask, i] = 1 - distances[mask]['distance']/300
# mask = distances['distance'] < 10
# hex_colors[mask] = (1, 1, 1)
# hex_colors.shape = (400, 3)

# center_cords_color = np.hstack((center_cords, hex_colors), dtype=np.float32)
# center_cords_color_vbo = ctx.buffer(center_cords_color.tobytes())

topography_texture = import_texture("topography_05.png", "GRAY")
topography_array = np.array(topography_texture, dtype=np.uint32)
topography_buffer = ctx.buffer(topography_array.tobytes())
topography_buffer.bind_to_storage_buffer(0)
topography_colors = get_topography_colors_array()
new_id_prog['u_topography_colors'].write(topography_colors.tobytes())
new_id_prog['u_map_width'] = 37


line_colors = np.zeros((n_tiles, 3), dtype=np.float32)
line_colors_vbo = ctx.buffer(line_colors.tobytes())

# tile_vao = ctx.vertex_array(flat_color_prog, [(corner_offsets_vbo, '2f', 'in_position'),
#                                               (center_cords_color_vbo, '2f 3f /i', 'in_instance_position', 'in_color')])

tile_vao = ctx.vertex_array(new_id_prog, [(corner_offsets_vbo, '2f', 'in_position'),
                                              (hex_id_vbo, '2u /i', 'in_instance_id')])

grid_vao = ctx.vertex_array(flat_color_prog, [(corner_offsets_vbo, '2f', 'in_position'),
                                              (center_cords_vbo, '2f /i', 'in_instance_position'),
                                              (line_colors_vbo, '3f /i', 'in_color')])

fps_prog = ctx.program(import_shader("pos_texcoord.vert"), import_shader("texture.frag"))
quad_vertices = np.array([  # position (x, y), texture_coord (u, v), x-1 for some reason??? in_instance_position
    -1.0, -1.0, 0.0, 1.0,  # Bottom-left
    -1.0, -0.9, 0.0, 0.0,  # Top-left
    -0.8, -1.0, 1.0, 1.0,  # Bottom-right
    -0.8, -0.9, 1.0, 0.0  # Top-right
], dtype='f4')
fps_vbo = ctx.buffer(quad_vertices.tobytes())
fps_vao = ctx.vertex_array(ui_prog, [(fps_vbo, '2f 2f', 'in_position', 'in_texcoord')])

###############################################################################################################
#   # Game Loop
###############################################################################################################

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                last_pos_for_scroll = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                last_pos_for_scroll = None
        elif event.type == pygame.MOUSEMOTION:
            # Handle scrolling
            if last_pos_for_scroll is not None:
                current_pos_snapshot = event.pos
                scroll.x -= current_pos_snapshot[0] - last_pos_for_scroll[0]
                scroll.y -= current_pos_snapshot[1] - last_pos_for_scroll[1]
                last_pos_for_scroll = current_pos_snapshot
        elif event.type == pygame.MOUSEWHEEL:
            scroll.z += event.y * 0.5  # Scroll up (1) or down (-1), scaled by 0.5

    ctx.clear(0.1, 0.1, 0.1)

    new_mvp_matrix = mvp.update().to_bytes()
    new_id_prog['u_mvp_matrix'].write(new_mvp_matrix)
    flat_color_prog['u_mvp_matrix'].write(new_mvp_matrix)
    tile_vao.render(moderngl.TRIANGLE_FAN, vertices=6, instances=n_tiles)
    grid_vao.render(moderngl.LINE_STRIP, vertices=4, instances=n_tiles)

    # fps = int(clock.get_fps())
    # my_text = f"fps: {fps} ModernGL"
    # texture_data = create_font_texture(my_text, font)
    # text_texture = ctx.texture(*texture_data)
    # text_texture.use(0)
    ctx.texture(*create_font_texture(f"fps: {int(clock.get_fps())} ModernGL", font)).use(0)
    fps_vao.render(moderngl.TRIANGLE_STRIP, vertices=4)

    pygame.display.flip()
    clock.tick(FPS_CAP)


pygame.quit()

all_to_be_released = [center_cords_vbo, corner_offsets_vbo, line_colors_vbo, fps_vbo,
                      flat_color_prog, ui_prog, grid_vao, tile_vao]

for i in all_to_be_released:
    i.release()














