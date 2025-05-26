#version 330

in vec2 v_uv;

uniform sampler2D u_texture;

out vec4 fragColor;

void main() {
    gl_FragColor = texture(u_texture, v_uv);
}
