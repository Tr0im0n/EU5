import pygame
import moderngl
import numpy as np

from src.hex_grid.hex_grid_class import HexGrid


# Initialize Pygame
pygame.init()
pygame.display.set_mode((1600, 900), pygame.OPENGL | pygame.DOUBLEBUF)
ctx = moderngl.create_context()

hex_grid2 = HexGrid(16, 9, (0.0, 0.0, 0.0))

vertex_shader = '''
#version 330 core
in vec2 in_cord;
void main() {
    gl_Position = vec4(0.05*in_cord.x-0.9, -0.05*in_cord.y+0.8, 0.0, 1.0);
}
'''

fragment_shader = '''
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
'''

# Create shader program
prog = ctx.program(
    vertex_shader=vertex_shader,
    fragment_shader=fragment_shader
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.0, 0.0, 0.0)  # Black background

    ctx.line_width = 2.0

    array_copy = hex_grid2.lines_cords.flatten().astype(np.float32)
    vbo = ctx.buffer(array_copy)
    vao = ctx.vertex_array(prog, [(vbo, '2f', 'in_cord')])
    for i in range(155):
        vao.render(moderngl.LINE_STRIP, vertices=4, first=i*4)

    pygame.display.flip()

# Cleanup
vao.release()
vbo.release()
prog.release()
pygame.quit()


