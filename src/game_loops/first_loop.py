import moderngl
import numpy as np
import pygame
from pyglm import glm

from src.game_loops.scroll import Scroll
from src.hex_grid.hex_grid_class import HexGrid
from utils.import_asset import import_csv, import_shader

pygame.init()
WIDTH, HEIGHT = 1600, 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)
running = True

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Pygame Boilerplate")
ctx = moderngl.create_context()

last_pos_for_scroll = None
scroll = Scroll()

# ModernGL vbo, prog, vao
hex_grid2 = HexGrid(20, 20, WHITE)
center_cords = hex_grid2.center_cords
center_cords_vbo = ctx.buffer(center_cords.flatten().astype(np.float32))
line_offsets_vbo = ctx.buffer(hex_grid2.corner_offsets[2:10])
tile_offsets_vbo = ctx.buffer(hex_grid2.corner_offsets)
hex_colors = import_csv("korea_manchuria_hires.csv")
hex_colors_vbo = ctx.buffer(hex_colors)

tile_prog = ctx.program(import_shader("tiles_color.vert"), import_shader("color.frag"))
grid_prog = ctx.program(import_shader("grid.vert"), import_shader("white.frag"))



all_to_be_released = [center_cords_vbo, line_offsets_vbo, tile_offsets_vbo, hex_colors_vbo,
                      tile_prog, grid_prog]

# universal

camera_pos = glm.vec3(0.0, -5.0, 5.0)  # Camera at (0,0,15)
look_at = glm.vec3(0.0, 0.0, 0.0)  # Looking at the origin
up_vector = glm.vec3(0.0, 1.0, 0.0)  # Y-axis is up
view_matrix = glm.lookAt(camera_pos, look_at, up_vector)

fovy_deg = 45.0
screen_width, screen_height = 1600, 900
aspect_ratio = screen_width / screen_height
near_plane, far_plane = 1.0, 100.0
projection_matrix = glm.perspective(glm.radians(fovy_deg), aspect_ratio, near_plane, far_plane)

model_matrix = glm.mat4(1.0)
model_matrix = glm.scale(model_matrix, glm.vec3(0.1, -0.1, 0.1))

for prog in [tile_prog, grid_prog]:
    prog['u_model'].write(model_matrix.to_bytes())
    prog['u_view'].write(view_matrix.to_bytes())
    prog['u_projection'].write(projection_matrix.to_bytes())


tile_vao = ctx.vertex_array(tile_prog, [(tile_offsets_vbo, '2f', 'in_position'),
                                        (hex_colors_vbo, '3f/i', 'in_color'),
                                        (center_cords_vbo, '2f/i', 'in_instance_position')])

grid_vao = ctx.vertex_array(grid_prog, [(line_offsets_vbo, '2f', 'in_position'),
                                        (center_cords_vbo, '2f/i', 'in_instance_position')])


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

    # fps = str(int(clock.get_fps()))
    # fps_text = font.render(f"fps: {fps}", True, WHITE)
    #
    # screen.fill(BLACK)
    # hex_grid2.draw(screen, scroll, 40, 30)
    #
    # screen.blit(fps_text, (10, 10))

    # camera_pos = glm.vec3(0.0, -3.0, 5.0)  # Camera at (0,0,15)
    scrolled_camera_pos = camera_pos + glm.vec3(scroll.x/200, -scroll.y/200, -scroll.z)
    # look_at = glm.vec3(0.0, 0.0, 0.0)  # Looking at the origin
    scrolled_look_at = look_at + glm.vec3(scroll.x/200, -scroll.y/200, 0)
    view_matrix = glm.lookAt(scrolled_camera_pos, scrolled_look_at, up_vector)
    tile_prog['u_view'].write(view_matrix.to_bytes())
    grid_prog['u_view'].write(view_matrix.to_bytes())

    tile_vao = ctx.vertex_array(tile_prog, [(tile_offsets_vbo, '2f', 'in_position'),
                                            (hex_colors_vbo, '3f/i', 'in_color'),
                                            (center_cords_vbo, '2f/i', 'in_instance_position')])

    tile_vao.render(moderngl.TRIANGLE_FAN, vertices=6, instances=400)
    grid_vao.render(moderngl.LINE_STRIP, vertices=4, instances=400)

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()

for i in all_to_be_released:
    i.release()
