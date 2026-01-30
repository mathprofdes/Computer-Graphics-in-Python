#version 330 core

/**
Fragment shader that blends two textures.

[in] color --- vec4 vertex color from memory.
[in] tex_coord --- vec2 texture coordinate from memory.

[out] fColor --- vec4 output color to the frame buffer.

[uniform] useTexture --- boolean that determines if the texture is used.
[uniform] tex1 --- sampler2D, the texture.
[uniform] tex2 --- sampler2D, the texture.

*/

in vec4 color;
in vec2 tex_coord;

uniform sampler2D tex1;
uniform sampler2D tex2;
uniform bool useTexture;

out vec4 fColor;

void main()
{
    if (useTexture)
        fColor = 0.5*texture(tex1, tex_coord) + 0.5*texture(tex2, tex_coord);
    else
        fColor = color;

    fColor = min(fColor, vec4(1.0));
}
