#version 330 core

in vec2 in_position;
in vec2 in_instance_position;
in vec3 in_color;
in vec2 in_texcoord;

out vec3 v_color;
out vec2 v_texcoord;

uniform bool u_use_instance_position;
uniform bool u_use_mvp;
uniform mat4 u_mvp_matrix;

void main() {
    vec4 local_position = vec4(in_position + in_instance_position, 0, 1.0);

    if (u_use_mvp){
        gl_Position = u_mvp_matrix * local_position;
    } else {
        gl_Position = local_position;
    }

    v_color = in_color;
    v_texcoord = in_texcoord;
}


//    if (u_use_instance_position){
//        vec4 local_position = vec4(in_position + in_instance_position, 0, 1.0);
//    } else {
//        vec4 local_position = vec4(in_position, 0, 1.0);
//    }

