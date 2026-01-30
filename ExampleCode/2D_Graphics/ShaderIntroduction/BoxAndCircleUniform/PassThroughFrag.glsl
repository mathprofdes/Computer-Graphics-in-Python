#version 330 core

/**
Simple pass through fragment shader.

[in] color --- vec4 color from vertex shader.

[out] fColor --- vec4 output color to the frame buffer.
*/

in  vec4 color;
out vec4 fColor;

void main()
{
    fColor = color;
}
