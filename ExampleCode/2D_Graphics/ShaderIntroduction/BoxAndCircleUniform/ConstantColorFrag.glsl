#version 330 core

/**
Simple constant color shader.

ConstantColor --- uniform variable for a single color.

*/

uniform vec4 ConstantColor;
out vec4 col;

void main()
{
    col = ConstantColor;
}
