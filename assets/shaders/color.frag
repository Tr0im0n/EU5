#version 330

flat in vec3 v_color;

out vec4 fragColor;

void main() {
    gl_FragColor = vec4(v_color, 1.);
}
