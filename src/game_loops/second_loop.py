import moderngl
import numpy as np
import pygame
from pyglm import glm

from src.hex_grid.hex_map import HexMap
from src.random.font_texture import create_font_texture
from src.random.model_view_projection import MVP
from src.random.scroll import Scroll
from utils.import_asset import import_shader

# Constants
WIDTH, HEIGHT = 1600, 900
FPS_CAP = 60
# Pygame + ModernGL
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
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

###############################################################################################################
#   # Making VAO 's
###############################################################################################################

hex_map_1 = HexMap(20, 20)
center_cords = hex_map_1.center_cords.astype(np.float32)
center_cords.shape = (400, 2)
corner_offsets_vbo = ctx.buffer(hex_map_1.corner_offsets.tobytes())

distances = hex_map_1.distances
hex_colors = np.zeros((20, 20, 3), dtype=np.float32)
for i in (0, 1, 2):
    mask = distances['start_node'] == i
    hex_colors[mask, i] = 1 - distances[mask]['distance']/300

mask = distances['distance'] < 10
hex_colors[mask] = (1, 1, 1)

hex_colors.shape = (400, 3)

center_cords_color = np.hstack((center_cords, hex_colors), dtype=np.float32)
center_cords_color_vbo = ctx.buffer(center_cords_color.tobytes())

line_colors = np.zeros((400, 3), dtype=np.float32)
line_colors_vbo = ctx.buffer(line_colors.tobytes())

tile_vao = ctx.vertex_array(flat_color_prog, [(corner_offsets_vbo, '2f', 'in_position'),
                                              (center_cords_color_vbo, '2f 3f /i', 'in_instance_position', 'in_color')])

grid_vao = ctx.vertex_array(flat_color_prog, [(corner_offsets_vbo, '2f', 'in_position'),
                                              (center_cords_color_vbo, '2f 3x4 /i', 'in_instance_position'),
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

    ctx.clear(0.0, 0.0, 0.0)

    flat_color_prog['u_mvp_matrix'].write(mvp.update().to_bytes())
    tile_vao.render(moderngl.TRIANGLE_FAN, vertices=6, instances=400)
    grid_vao.render(moderngl.LINE_STRIP, vertices=4, instances=400)

    fps = int(clock.get_fps())
    my_text = f"fps: {fps} ModernGL"
    texture_data = create_font_texture(my_text, font)
    text_texture = ctx.texture(*texture_data)
    text_texture.use(0)
    fps_vao.render(moderngl.TRIANGLE_STRIP, vertices=4)

    pygame.display.flip()
    clock.tick(FPS_CAP)


pygame.quit()

all_to_be_released = [center_cords_color_vbo, corner_offsets_vbo, line_colors_vbo, fps_vbo,
                      flat_color_prog, ui_prog, grid_vao, tile_vao]

for i in all_to_be_released:
    i.release()














