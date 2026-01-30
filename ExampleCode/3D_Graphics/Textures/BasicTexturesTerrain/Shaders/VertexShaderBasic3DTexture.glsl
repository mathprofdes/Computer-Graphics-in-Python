#version 330 core

/**
Vertex shader that incorporates the transformation of vertices
by a projection*view*model matrix.

[in] position --- vec4 vertex position from memory.
[in] icolor --- vec4 vertex color from memory.

[out] color --- vec4 output color to the fragment shader.

[uniform] ProjView --- mat4 projection and view matrix.
[uniform] Model --- mat4 model matrix.

*/

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 icolor;
layout(location = 3) in vec2 itex;

uniform mat4 ProjView = mat4(1);
uniform mat4 Model = mat4(1);

out vec4 color;
out vec2 tex_coord;

void main()
{
    color = icolor;
    tex_coord = itex;
    gl_Position = ProjView * Model * position;
}
