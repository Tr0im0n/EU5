#version 330 core

in vec3 v_color;
in vec2 v_texcoord;

out vec4 fragColor;

uniform bool u_use_u_color;
uniform bool u_use_texture;
uniform vec4 u_color;
uniform sampler2D u_texture_sampler;    // NEW: Uniform for the texture

void main() {
    if (u_use_u_color) {   // Mode 1: Render the grid (fixed white color)
        fragColor = u_color;
    } else if (u_use_texture) {     // Mode 2: Render textured objects
        fragColor = texture(u_texture_sampler, v_texcoord);
    } else {    // Mode 3: Render non-textured (plain colored) tiles
        fragColor = vec4(v_color, 1.0);
    }
}