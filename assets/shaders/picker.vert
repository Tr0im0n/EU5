#version 430 core

in vec2 in_position;
in uvec2 in_instance_id;

flat out vec3 v_color;

layout(std140, binding = 0) uniform MyMat {
    mat4 u_mvp_matrix;
};

void main() {
    vec2 instance_position;
    instance_position.x = 2*in_instance_id.x + in_instance_id.y%2;
    instance_position.y = 3*in_instance_id.y;
    gl_Position = u_mvp_matrix * vec4(in_position+instance_position, 0, 1.0);

    v_color = vec3(1, in_instance_id);
}