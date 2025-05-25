import os

import pygame
import moderngl
import numpy as np
from pyglm import glm  # Import PyGLM
from src.hex_grid.hex_grid_class import HexGrid


# Initialize Pygame
pygame.init()
screen_width, screen_height = 1600, 900
pygame.display.set_mode((screen_width, screen_height), pygame.OPENGL | pygame.DOUBLEBUF)
ctx = moderngl.create_context()

hex_grid2 = HexGrid(16, 9, (0.0, 0.0, 0.0))
"""
Get RAW coordinates from your HexGrid (no scaling/scrolling on CPU)
Assume your HexGrid returns coordinates that represent its actual 3D position (x, y, z=0 for now)
You might need to adjust your HexGrid to produce reasonable initial world coordinates
For demonstration, let's pretend your lines_cords are already 'world' coordinates
For a 2D grid, initially set Z to 0.0 or a small constant like -1.0.
If your get_lines_cords produces (N, 4, 2), you'll want (N, 4, 3) for Z.
Let's add a Z component to the raw assets, assuming it's flat on Z=0
Adjust this based on how your HexGrid actually generates initial coords.
"""
raw_coords_2d = hex_grid2.lines_cords.flatten().astype(np.float32)

# Convert 2D (x,y) to 3D (x,y,z) for OpenGL (z=0.0)
# This assumes your hex_grid2.lines_cords are already in a reasonable "world" scale.
# You might need to add a scaling factor here if your hex_grid produces very small/large numbers
# e.g., raw_coords_2d * 0.1 or similar, to fit in a typical 3D scene.
coords_3d = np.zeros((raw_coords_2d.size // 2, 3), dtype=np.float32)
coords_3d[:, :2] = raw_coords_2d.reshape(-1, 2)
# You can give different Z values here if you want some hexes to appear closer/further
# e.g., coords_3d[:, 2] = np.sin(coords_3d[:, 0] * 0.1) * 5.0 # For wavy grid
# Or simply:
coords_3d[:, 2] = 0.0 # All on the Z=0 plane initially

# Flatten again for VBO
final_vbo_data = coords_3d.flatten()

current_script_path = os.path.abspath(__file__)
root_directory = os.path.join(current_script_path, "..", "..", "..")

with open(os.path.join(root_directory, 'assets', 'shaders', 'mvp.vert'), 'r') as file:
    vertex_shader = file.read()

with open(os.path.join(root_directory, 'assets', 'shaders', 'white.frag'), 'r') as file:
    fragment_shader = file.read()

prog = ctx.program(vertex_shader, fragment_shader)

vbo = ctx.buffer(final_vbo_data)
# Note: '3f' because in_position is now a vec3
vao = ctx.vertex_array(prog, [(vbo, '3f', 'in_position')])

# Get uniform locations (do this once)
u_model_loc = prog['u_model']
u_view_loc = prog['u_view']
u_projection_loc = prog['u_projection']

# --- Set up Camera (View Matrix) ---
camera_pos = glm.vec3(0.0, -3.0, 5.0)   # Camera at (0,0,15)
look_at = glm.vec3(0.0, 0.0, 0.0)    # Looking at the origin
up_vector = glm.vec3(0.0, 1.0, 0.0)  # Y-axis is up
view_matrix = glm.lookAt(camera_pos, look_at, up_vector)

# --- Set up Projection Matrix ---
# Field of View (FoV) in degrees (vertical)
fovy_deg = 45.0
# Aspect ratio (screen width / screen height)
aspect_ratio = screen_width / screen_height
# Near and Far clipping planes (objects closer than near or further than far are cut off)
near_plane = 0.1
far_plane = 100.0
projection_matrix = glm.perspective(glm.radians(fovy_deg), aspect_ratio, near_plane, far_plane)

# --- Set up Model Matrix (for your hex grid) ---
# Start with identity matrix (no translation, rotation, scale)
model_matrix = glm.mat4(1.0)
print(model_matrix)
# You can then translate, rotate, or scale your grid
# model_matrix = glm.translate(model_matrix, glm.vec3(0.0, 0.0, 0.0))
# model_matrix = glm.rotate(model_matrix, glm.radians(45.0), glm.vec3(0.0, 1.0, 0.0)) # Rotate around Y axis
# model_matrix = glm.scale(model_matrix, glm.vec3(0.1, 0.1, 0.1)) # Scale down to fit view

# If your hex grid is huge in world units, you'll need to scale it down,
# either by adjusting initial `coords_3d` or using `glm.scale` on `model_matrix`.
# Example: If your raw hex coords are like (0-16, 0-9), they are too large for -10 to 10 view range.
# Scale them down so they fit well in the camera's view.
# A simple way to scale:
model_scale = 0.1 # Adjust this based on your HexGrid's coordinate range
model_matrix = glm.scale(model_matrix, glm.vec3(model_scale, -model_scale, model_scale))
# And translate to center it
model_matrix = glm.translate(model_matrix, glm.vec3(-8.0, -9.0, 0.0)) # Center 16x9 grid
print(model_matrix)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    ctx.clear(0.0, 0.0, 0.0)
    ctx.line_width = 2.0

    # Pass matrices to the shader
    u_model_loc.write(model_matrix.to_bytes())
    u_view_loc.write(view_matrix.to_bytes())
    u_projection_loc.write(projection_matrix.to_bytes())

    total_vertices = final_vbo_data.size // 3 # Now 3 floats per vertex (x,y,z)
    vao.render(moderngl.LINES, vertices=total_vertices) # Assuming LINES for individual segments

    pygame.display.flip()

# Cleanup
vao.release()
vbo.release()
prog.release()
pygame.quit()