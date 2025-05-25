#version 330 core

in vec2 in_position;
in vec2 in_instance_position;

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

void main() {
    gl_Position = u_projection * u_view * u_model * vec4(in_position+in_instance_position, 0.01, 1.0);
}