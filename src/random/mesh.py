import moderngl
import numpy as np
import pygame # For texture loading helper

class Mesh:
    def __init__(self, ctx, vertices, program, vao_format, mode=moderngl.TRIANGLES, texture=None):
        self.ctx = ctx
        self.program = program
        self.mode = mode
        self.texture = texture

        # Create a VBO from vertices
        self.vbo = ctx.buffer(vertices.astype('f4').tobytes())

        # Create a VAO linking VBO attributes to shader inputs
        # vao_format is a list of tuples: (buffer, layout, *attribute_names)
        # Example: [(self.vbo, '3f 3f 2f', 'in_position', 'in_normal', 'in_texcoord')]
        self.vao = ctx.vertex_array(self.program, vao_format)

    def render(self, projection_matrix, view_matrix, model_matrix):
        """
        Renders the mesh. Assumes common uniform names for matrices.
        """
        # Activate the program
        self.program.use()

        # Pass uniforms (matrices) to the shader
        try:
            self.program['projection'].write(projection_matrix.astype('f4').tobytes())
            self.program['view'].write(view_matrix.astype('f4').tobytes())
            self.program['model'].write(model_matrix.astype('f4').tobytes())
        except KeyError as e:
            # Handle cases where shaders might not have all uniforms
            # print(f"Warning: Shader missing uniform {e}")
            pass

        # Bind texture if available
        if self.texture:
            self.texture.use(0) # Use texture unit 0
            self.program['u_texture'].value = 0 # Tell shader to use unit 0

        # Render the VAO
        self.vao.render(self.mode)

    def release(self):
        """
        Releases the ModernGL resources held by the mesh.
        Call this when the mesh is no longer needed to prevent memory leaks.
        """
        self.vbo.release()
        self.vao.release()


