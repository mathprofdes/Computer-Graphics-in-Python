#version 410 core

/**
Fragment shader that blends up to 10 textures.

[in] color --- vec4 vertex color from memory.
[in] tex_coord --- vec2 texture coordinate from memory.

[out] fColor --- vec4 output color to the frame buffer.

[uniform] useTexture --- Array of boolean that determines if the texture is used.
[uniform] tex --- Array of sampler2D texture locations.

*/

in vec4 color;
in vec2 tex_coord;

uniform sampler2D tex[10];
uniform bool useTexture[10];

out vec4 fColor;

void main()
{
    int textureCount = 0;
    for (int i = 0; i < 10; i++)
        if (useTexture[i])
            textureCount++;

    vec4 texColor = vec4(0.0);

    for (int i = 0; i < 10; i++)
        if (useTexture[i])
            texColor += 1.0/textureCount * texture(tex[i], tex_coord);

    fColor = min(texColor, vec4(1.0));
}


//  Prior to GLSL 4.1 the index for texture arrays must be constants.  So the
//  equivalent for the lest for loop would be below.
/*
    if (useTexture[0])
        texColor += 1.0/textureCount * texture(tex[0], tex_coord);
    if (useTexture[1])
        texColor += 1.0/textureCount * texture(tex[1], tex_coord);
    if (useTexture[2])
        texColor += 1.0/textureCount * texture(tex[2], tex_coord);
    if (useTexture[3])
        texColor += 1.0/textureCount * texture(tex[3], tex_coord);
    if (useTexture[4])
        texColor += 1.0/textureCount * texture(tex[4], tex_coord);
    if (useTexture[5])
        texColor += 1.0/textureCount * texture(tex[5], tex_coord);
    if (useTexture[6])
        texColor += 1.0/textureCount * texture(tex[6], tex_coord);
    if (useTexture[7])
        texColor += 1.0/textureCount * texture(tex[7], tex_coord);
    if (useTexture[8])
        texColor += 1.0/textureCount * texture(tex[8], tex_coord);
    if (useTexture[9])
        texColor += 1.0/textureCount * texture(tex[9], tex_coord);
// */
