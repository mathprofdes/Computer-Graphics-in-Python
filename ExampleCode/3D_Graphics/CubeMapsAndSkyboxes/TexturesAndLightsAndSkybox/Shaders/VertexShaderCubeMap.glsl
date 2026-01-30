#version 330 core

/**
Vertex shader specifically for a cub map texture.  Incorporates
the transformation of vertices by a projection*view*model matrix. Sets
the texture coordinate to the position of the vertex.

[in] vposition --- vec4 vertex position from memory.
[out] tex_coord --- vec3 pass through of the texture coordinates.
[uniform] PVM --- mat4 transformation matrix in the form projection*view*model.

*/

layout(location = 0) in vec4 vposition;

uniform mat4 PV;

out vec3 tex_coord;

void main()
{
    tex_coord = vec3(vposition);
    gl_Position = PV * vposition;
}
