#version 330 core

/**
Vertex shader that incorporates the transformation of vertices
by a projection*view*model matrix.

[in] position --- vec4 vertex position from memory.
[in] icolor --- vec4 vertex color from memory.

[out] color --- vec4 output color to the fragment shader.

[uniform] PVM --- mat4 projection, view, and model matrix.


*/

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 icolor;

uniform mat4 PVM = mat4(1);

out vec4 color;

void main()
{
    color = icolor;
    gl_Position = PVM * position;
}
