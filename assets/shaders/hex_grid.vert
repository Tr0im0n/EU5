#version 330 core

in vec2 in_position;
in vec2 in_uv;

out vec2 v_uv;

void main() {
    gl_Position = vec4(0.5*in_position.x, 0.5*in_position.y, 1.0, 1.0);
    v_uv = in_uv;
}