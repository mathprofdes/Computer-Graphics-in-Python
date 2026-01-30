#version 330 core

/**
Dual purpose fragment shader, can act like a pass through fragment shader
or a constant color fragment shader.

[in] color --- vec4 color from vertex shader.
[out] col --- vec4 color that will be sent to the frame buffer.

info --- Uniform struct type holding the mode to use and the constant color.

*/

struct Information
{
    int pass;
    vec4 constantColor;
};

in vec4 color;
out vec4 col;

uniform Information info;

void main()
{
    if (info.pass != 0)
        col = color;
    else
        col = info.constantColor;
}
