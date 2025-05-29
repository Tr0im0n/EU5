#version 330 core

in vec2 in_position;
in vec2 in_instance_position;
in vec3 in_color;

out vec3 v_color;

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

void main() {
    gl_Position = u_projection * u_view * u_model * vec4(in_position+in_instance_position, 0, 1.0);
    v_color = in_color;
}