#version 330 core

/**
Shader that allows the use of pass through or constant color.

[in] color --- vec4 color from vertex shader.
[out] fColor --- vec4 output color to the frame buffer.

ConstantColor --- uniform variable for a single color.
passcolor --- uniform variable for selecting the method for rendering.

*/

in  vec4 color;
out vec4 col;

uniform vec4 ConstantColor;
uniform bool passcolor = true;

void main()
{
    if (passcolor)
        col = color;
    else
        col = ConstantColor;
}
