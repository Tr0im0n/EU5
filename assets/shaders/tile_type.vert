#version 430 core

in vec2 in_position;
in uvec2 in_instance_id;

flat out vec3 v_color;

uniform vec3 u_topography_colors[6];
uniform mat4 u_mvp_matrix;
uniform uint u_map_width;

layout(std430, binding = 0) buffer MyUintData {
    uint data_array[];
};

void main() {
    vec2 instance_position;
    instance_position.x = 2*in_instance_id.x + in_instance_id.y%2;
    instance_position.y = 3*in_instance_id.y;
    gl_Position = u_mvp_matrix * vec4(in_position+instance_position, 0, 1.0);

    uint color_type = data_array[in_instance_id.y * u_map_width + in_instance_id.x];
    v_color = u_topography_colors[color_type];
}