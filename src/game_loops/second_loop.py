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

###############################################################################################################
#   # Making VAO 's
###############################################################################################################
# Shader Programs
new_id_prog = ctx.program(import_shader("tile_type.vert"), import_shader("color.frag"))
hex_grid_prog = ctx.program(import_shader("instance_mvp.vert"), import_shader("uniform_color.frag"))
hex_grid_prog['u_color'] = np.zeros(4, dtype=np.float32)
ui_prog = ctx.program(import_shader("pos_texcoord.vert"), import_shader("texture.frag"))
# mvp ubo
mvp_ubo = ctx.buffer(mvp.update().to_bytes(), dynamic=True)
mvp_ubo.bind_to_uniform_block(0)

# hex map info
width = 18 # 37
height = 21 # 42
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

topography_texture = import_texture("topography_05_small.png", "GRAY")
topography_array = np.array(topography_texture, dtype=np.uint32)
topography_buffer = ctx.buffer(topography_array.tobytes())
topography_buffer.bind_to_storage_buffer(0)
topography_colors = get_topography_colors_array()
new_id_prog['u_topography_colors'].write(topography_colors.tobytes())
new_id_prog['u_map_width'] = width


tile_vao = ctx.vertex_array(new_id_prog, [(corner_offsets_vbo, '2f', 'in_position'),
                                              (hex_id_vbo, '2u /i', 'in_instance_id')])

hex_grid_vao = ctx.vertex_array(hex_grid_prog, [(corner_offsets_vbo, '2f', 'in_position'),
                                                (center_cords_vbo, '2f /i', 'in_instance_position')])

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
#   # Picker!
###############################################################################################################

picking_texture = ctx.texture((SCREEN_WIDTH, SCREEN_HEIGHT), 4, dtype='f1')
picking_depth_attachment = ctx.depth_texture((SCREEN_WIDTH, SCREEN_HEIGHT)) # Same size as screen

fbo_picking = ctx.framebuffer(
    color_attachments=[picking_texture],
    depth_attachment=picking_depth_attachment
)

picker_prog = ctx.program(import_shader("picker.vert"), import_shader("color.frag"))
vao_picking = ctx.vertex_array(picker_prog, [(corner_offsets_vbo, '2f', 'in_position'),
                                              (hex_id_vbo, '2u /i', 'in_instance_id')])


# picker_vbo = 0
# picker_vao = ctx.vertex_array(flat_color_prog, [(fps_vbo, '2f 2f', 'in_position', 'in_texcoord')])


###############################################################################################################
#   # Game Loop
###############################################################################################################

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # PICKER
                mouse_x, mouse_y = event.pos
                fbo_picking.use()
                ctx.clear(0.0, 0.0, 0.0, 1.0)  # Clear picking FBO with black (Type=0, X=0, Y=0)
                vao_picking.render(moderngl.TRIANGLE_FAN, vertices=6, instances=n_tiles)
                # ctx.enable(moderngl.DEPTH_TEST)
                gl_y = SCREEN_HEIGHT - 1 - mouse_y  # Convert mouse_y to OpenGL's bottom-up coords
                pixel = fbo_picking.read(
                    viewport=(mouse_x, gl_y, 1, 1),
                    components=4,
                    dtype='f1'  # Read as unsigned bytes (uint8)
                )
                picked_color_bytes = np.frombuffer(pixel, dtype=np.uint8)
                print(picked_color_bytes)
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

    ctx.screen.use()
    ctx.clear(0.1, 0.1, 0.1)

    mvp_ubo.write(mvp.update().to_bytes())

    tile_vao.render(moderngl.TRIANGLE_FAN, vertices=6, instances=n_tiles)
    hex_grid_vao.render(moderngl.LINE_STRIP, vertices=4, instances=n_tiles)
    # longer version in bottom comment
    ctx.texture(*create_font_texture(f"fps: {int(clock.get_fps())} ModernGL", font)).use(0)
    fps_vao.render(moderngl.TRIANGLE_STRIP, vertices=4)

    pygame.display.flip()
    clock.tick(FPS_CAP)


pygame.quit()

all_to_be_released = [center_cords_vbo, corner_offsets_vbo, fps_vbo,
                      hex_grid_prog, ui_prog, hex_grid_vao, tile_vao]

for i in all_to_be_released:
    i.release()



"""

    fps = int(clock.get_fps())
    my_text = f"fps: {fps} ModernGL"
    texture_data = create_font_texture(my_text, font)
    text_texture = ctx.texture(*texture_data)
    text_texture.use(0)


"""










