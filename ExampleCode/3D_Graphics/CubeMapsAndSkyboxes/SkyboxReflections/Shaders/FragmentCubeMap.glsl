#version 330 core

/**
Fragment shader that is specific for a cube map.

[in] tex_coord --- vec3 texture coordinate from the vertex shader.
[out] fColor --- vec4 output color to the frame buffer.
[uniform] cmtex --- samplerCube, the texture.

*/

in vec3 tex_coord;

uniform samplerCube cmtex;

out vec4 fColor;

void main()
{
    fColor = texture(cmtex, tex_coord);
}
