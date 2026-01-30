#version 330 core

/**
Fragment shader that calculates the majority of the Phong lighting model.
Developeed for processing Wavefront OBJ models.  The lighting does not calculate
spot lights or attenuation, for better processing speed.  There are three textures
that are possible in the OBJ Models, a texture applied to an ambient, diffuse, and
specular portions of the light.  We use multiplaction of the material values times
the texture value so that the texture intensity is scaled by the material.

[in] position --- vec4 vertex position from memory.
[in] color --- vec4 vertex color from memory.
[in] normal --- vec3 normal vector from memory.
[in] tex_coord --- vec2 texture coordinate from memory.

[out] fColor --- vec4 output color to the frame buffer.

[uniform] Lt --- Light struct containing a single light attribute set.
[uniform] Mat --- Material struct containing a single material attribute set.
[uniform] eye --- vec3 position of the viewer/camera.
[uniform] numLights --- Number of lights to use.

[uniform] useATex --- If the ambient texture is being used.
[uniform] useDTex --- If the diffuse texture is being used.
[uniform] useSTex --- If the specular texture is being used.

[uniform] sampler2D atex ---  Ambient texture.
[uniform] sampler2D dtex ---  Diffuse texture.
[uniform] sampler2D stex ---  Specular texture.

*/


struct Light
{
    bool on;///< Light on or off.
    vec4 position;///< Position of the light.
    vec3 spotDirection;///< Direction of the spot light.
    vec4 ambient;///< Ambient color of the light.
    vec4 diffuse;///< Diffuse color of the light.
    vec4 specular;///< Specular color of the light.
    float spotCutoff;///< Spot cutoff angle.
    float spotExponent;///< Spot falloff exponent.
    vec3 attenuation;///< Attenuation vector, x = constant, y = linear, z = quadratic.
};

struct Material
{
    vec4 ambient;///< Ambient color of the material.
    vec4 diffuse;///< Diffuse color of the material.
    vec4 specular;///< Specular color of the material.
    vec4 emission;///< Emission color of the material.
    float shininess;///< Shininess exponent of the material.
};

in vec4 position;
in vec4 color;
in vec3 normal;
in vec2 tex_coord;

uniform Light Lt[10];
uniform Material Mat;
uniform vec3 eye;
uniform int numLights;

uniform bool useATex = false;
uniform bool useDTex = false;
uniform bool useSTex = false;
uniform sampler2D atex;
uniform sampler2D dtex;
uniform sampler2D stex;

out vec4 fColor;

void main()
{
    float deg = 0.017453292519943296;

    vec4 cc = vec4(0.0);
    bool usingLights = false;
    vec4 ambientPortion = vec4(0, 0, 0, 0);
    vec4 diffusePortion = vec4(0, 0, 0, 0);
    vec4 specularPortion = vec4(0, 0, 0, 0);

    for (int i = 0; i < numLights; i++)
    {
        if (Lt[i].on)
        {
            usingLights = true;
            vec3 n = normalize(normal);
            vec3 l = normalize(vec3(Lt[i].position)-vec3(position));
            vec3 r = normalize(2.0*dot(l, n)*n - l);
            vec3 v = normalize(eye-vec3(position));

            float dfang = max(0.0, dot(l, n));
            float specang = max(0.0, dot(r, v));
            if (dfang == 0)
                specang = 0;

            ambientPortion += Mat.ambient*Lt[i].ambient;
            diffusePortion += Mat.diffuse*Lt[i].diffuse*dfang;
            specularPortion += Mat.specular*Lt[i].specular*pow(specang, Mat.shininess);
        }
    }

    if (useATex)
        ambientPortion = ambientPortion * texture(atex, tex_coord);

    if (useDTex)
        diffusePortion = diffusePortion * texture(dtex, tex_coord);

    if (useSTex)
        specularPortion = specularPortion * texture(stex, tex_coord);

    cc = ambientPortion + diffusePortion + specularPortion + Mat.emission;

    if (usingLights)
        fColor = cc;
    else
        fColor = color;

    fColor = min(fColor, vec4(1.0));
}
