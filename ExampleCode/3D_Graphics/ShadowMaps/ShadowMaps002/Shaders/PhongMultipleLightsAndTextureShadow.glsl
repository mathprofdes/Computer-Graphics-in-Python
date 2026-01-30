#version 330 core

/**
Fragment shader that calculates Phong lighting for each fragment,
textual for the same fragment and combines the two.

[in] position --- vec4 vertex position from memory.
[in] color --- vec4 vertex color from memory.
[in] normal --- vec3 normal vector from memory.
[in] tex_coord --- vec2 texture coordinate from memory.

[out] fColor --- vec4 output color to the frame buffer.

[uniform] Lt --- Light struct containing a single light attribute set.
[uniform] Mat --- Material struct containing a single material attribute set.
[uniform] eye --- vec3 position of the viewer/camera.
[uniform] GlobalAmbient --- vec4 global ambient color vector.
[uniform] useTexture --- boolean that determines if the texture is used.
[uniform] textrans --- mat4 texture transformation.
[uniform] tex1 --- sampler2D, the texture.

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
in vec4 FragPosLightSpace;

uniform Light Lt[10];
uniform Material Mat;
uniform vec3 eye;
uniform vec4 GlobalAmbient;
uniform int numLights;
uniform bool useTexture;
uniform mat4 textrans = mat4(1);

uniform sampler2D tex1;
uniform sampler2D shadowMap;

out vec4 fColor;

float ShadowCalculation(vec4 fragPosLightSpace)
{
    // perform perspective divide
    vec3 projCoords = fragPosLightSpace.xyz;// / fragPosLightSpace.w;
    // transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;
    // get closest depth value from light's perspective (using [0,1] range fragPosLight as coords)
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    // get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    // check whether current frag pos is in shadow


    //*
    vec3 lightDir = normalize(vec3(Lt[0].position)-vec3(position));
    float bias = max(0.05 * (1.0 - dot(normal, lightDir)), 0.005);
    // */

    //float bias = 0.005;

    //float shadow = currentDepth  > closestDepth  ? 1.0 : 0.0;
    //float shadow = currentDepth - bias  > closestDepth  ? 1.0 : 0.0;

    //*
    int softness = 1;
    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
    for (int x = -softness; x <= softness; ++x)
    {
        for (int y = -softness; y <= softness; ++y)
        {
            float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r;
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;
        }
    }
    shadow /= ((2*softness+1)*(2*softness+1));
    // */

    if (projCoords.z > 1.0)
        shadow = 0.0;

    return shadow;
}

void main()
{
    float deg = 0.017453292519943296;

    vec4 cc = vec4(0.0);
    bool usingLights = false;
    vec4 globalAmbientPortion = Mat.ambient*GlobalAmbient;

    float shadow = ShadowCalculation(FragPosLightSpace);

    for (int i = 0; i < numLights; i++)
    {
        if (Lt[i].on)
        {
            usingLights = true;
            vec3 n = normalize(normal);
            vec3 l = normalize(vec3(Lt[i].position)-vec3(position));
            vec3 r = normalize(2.0*dot(l, n)*n - l);
            vec3 v = normalize(eye-vec3(position));
            float lightDistance =length(vec3(Lt[i].position)-vec3(position));

            float dfang = max(0.0, dot(l, n));
            float specang = max(0.0, dot(r, v));
            if (dfang == 0)
            specang = 0;

            float attenuation = 1.0 / (Lt[i].attenuation[0] +
            Lt[i].attenuation[1] * lightDistance +
            Lt[i].attenuation[2] * lightDistance * lightDistance);

            float spotCos = dot(l, -normalize(Lt[i].spotDirection));
            float SpotCosCutoff = cos(Lt[i].spotCutoff*deg);// assumes that spotCutoff is in degrees

            float spotFactor = 1.0;
            if (spotCos < SpotCosCutoff && Lt[i].spotCutoff < 179.9)// Only fade if a spotlight
            {
                float range = 1 + SpotCosCutoff;
                spotFactor = pow(1 - (SpotCosCutoff - spotCos)/range, Lt[i].spotExponent);
            }

            vec4 ambientPortion = Mat.ambient*Lt[i].ambient;
            vec4 diffusePortion = Mat.diffuse*Lt[i].diffuse*dfang*attenuation*spotFactor;
            vec4 specularPortion = Mat.specular*Lt[i].specular*pow(specang, Mat.shininess)*attenuation*spotFactor;

            vec4 c = ambientPortion + diffusePortion + specularPortion;
            cc += min(c, vec4(1.0));
        }
    }

    cc = min(cc + globalAmbientPortion + Mat.emission, vec4(1.0));

    if (usingLights)
        fColor = cc;
    else
        fColor = color;

    if (useTexture)
    {
        vec4 texhom = vec4(tex_coord, 0, 1);
        vec4 transtex = textrans * texhom;
        vec2 transtex2 = vec2(transtex);

        fColor = 0.25*fColor + 0.75*texture(tex1, transtex2);
    }

    fColor = min(fColor, vec4(1.0));
    fColor = (1-0.6*shadow)*fColor;
}
