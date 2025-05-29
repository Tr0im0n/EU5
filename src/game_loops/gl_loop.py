import pygame
import moderngl
import numpy as np

from src.hex_grid.hex_grid_class import HexGrid
from utils.import_asset import import_shader, import_texture

def why_indents():
    # Initialize Pygame
    pygame.init()
    pygame.display.set_mode((1600, 900), pygame.OPENGL | pygame.DOUBLEBUF)
    ctx = moderngl.create_context()

    vertex_shader = '''
    #version 330 core
    in vec2 in_cord;
    in vec2 in_instance_cord;
    void main() {
        vec2 new_cord = in_cord+in_instance_cord;
        gl_Position = vec4(0.05*new_cord.x-0.9, 0.05*new_cord.y-0.8, 0.0, 1.0);
    }
    '''
    # -0.05*new_cord.y+0.8

    # Create shader program
    prog = ctx.program(vertex_shader=vertex_shader,
        fragment_shader=import_shader('white.frag'))

    prog2 = ctx.program(vertex_shader=import_shader("pos_uv.vert"),
        fragment_shader=import_shader('texture.frag'))

    hex_grid2 = HexGrid(16, 9, (0.0, 0.0, 0.0))

    instance_vbo = ctx.buffer(hex_grid2.center_cords.flatten().astype(np.float32))
    base_vbo = ctx.buffer(hex_grid2.corner_offsets[2:10])
    vao = ctx.vertex_array(prog, [(base_vbo, '2f', 'in_cord'), (instance_vbo, '2f/i', 'in_instance_cord')])

    image = import_texture("download_00.jpeg")
    my_texture = ctx.texture(image.size, 4, image.tobytes())

    # 3. (Optional but Recommended) Configure Texture Properties
    # Filtering: How pixels are sampled when the texture is scaled up/down
    # my_texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
    # Generate mipmaps for better quality at different distances
    # my_texture.build_mipmaps()
    # Wrapping: How UV coordinates outside the 0.0-1.0 range behave
    # my_texture.wrap_x = moderngl.REPEAT # Repeats the texture horizontally
    # my_texture.wrap_y = moderngl.REPEAT # Repeats the texture vertically

    my_texture.use(0)
    prog2['u_texture'].value = 0

    vert_vbo = ctx.buffer(hex_grid2.corner_offsets)

    # uv_data = np.array([
    #     # Triangle 1
    #     0.0, 0.0,  # Bottom-left UV
    #     1.0, 0.0,  # Bottom-right UV
    #     0.0, 1.0,  # Top-left UV
    #     1.0, 0.0,  # Bottom-right UV
    #     1.0, 1.0,  # Top-right UV
    #     0.0, 1.0,  # Top-left UV
    # ], dtype='f4')

    uv_data = np.array([
        0.5, 0.0,  # Top-left UV
        0.1, 0.25,  # Bottom-left UV
        0.1, 0.75,  # Bottom-right UV
        0.5, 1.0,  # Top-left UV
        0.9, 0.75,  # Bottom-right UV
        0.9, 0.25,  # Top-right UV
    ], dtype='f4')

    uv_data2 = np.array([
        193/593, 258/543,   # 259/543, 284/543
        116/593, 258/543,
        77/593, 191/543,
        116/593, 122/543,   # 121/543, 422/543
        193/593, 122/543,
        233/593, 191/543    # 191/543, 352/543
    ], dtype='f4')

    uv_vbo = ctx.buffer(uv_data2)

    tile_vao = ctx.vertex_array(prog2, [(vert_vbo, '2f', 'in_position'), (uv_vbo, '2f', 'in_uv')])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ctx.clear(0.0, 0.0, 0.0)  # Black background

        ctx.line_width = 2.0

        tile_vao.render(moderngl.TRIANGLE_FAN, vertices=6)

        vao.render(moderngl.LINE_STRIP, vertices=4, instances=144)

        pygame.display.flip()

    # Cleanup
    for i in [vao, instance_vbo, base_vbo, uv_vbo, vert_vbo, tile_vao, prog, prog2]:
        i.release()


    pygame.quit()


