#version 430 core

in vec2 in_position;
in vec2 in_instance_position;

layout(std140, binding = 0) uniform MyMat {
    mat4 u_mvp_matrix;
};

void main() {
    gl_Position = u_mvp_matrix * vec4(in_position+in_instance_position, 0.01, 1.0);
}