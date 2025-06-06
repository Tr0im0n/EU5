#version 430 core

in vec2 in_position;
in vec2 in_instance_position;
in vec3 in_color;

flat out vec3 v_color;

layout(std140, binding = 0) uniform MyMat {
    mat4 u_mvp_matrix;
};

void main() {
    gl_Position = u_mvp_matrix * vec4(in_position+in_instance_position, 0, 1.0);
    v_color = in_color;
}