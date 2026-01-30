#version 330 core

/**
Fragment shader that uses the Phong lighting model with a single light source.

[in] position --- vec4 vertex position from memory.
[in] color --- vec4 vertex color from memory.
[in] normal --- vec3 normal vector from memory.

[out] fColor --- vec4 output color to the frame buffer.

[uniform] Lt --- Light struct containing a single light attribute set.
[uniform] Mat --- Material struct containing a single material attribute set.
[uniform] eye --- vec3 position of the viewer/camera.
[uniform] GlobalAmbient --- vec4 global ambient color vector.

*/


struct Light
{
    bool on;             ///< Light on or off.
    vec4 position;       ///< Position of the light.
    vec3 spotDirection;  ///< Direction of the spot light.
    vec4 ambient;        ///< Ambient color of the light.
    vec4 diffuse;        ///< Diffuse color of the light.
    vec4 specular;       ///< Specular color of the light.
    float spotCutoff;    ///< Spot cutoff angle.
    float spotExponent;  ///< Spot falloff exponent.
    vec3 attenuation;    ///< Attenuation vector, x = constant, y = linear, z = quadratic.
};

struct Material
{
    vec4 ambient;     ///< Ambient color of the material.
    vec4 diffuse;     ///< Diffuse color of the material.
    vec4 specular;    ///< Specular color of the material.
    vec4 emission;    ///< Emission color of the material.
    float shininess;  ///< Shininess exponent of the material.
};

in vec4 position;
in vec4 color;
in vec3 normal;

uniform Light Lt;
uniform Material Mat;
uniform vec3 eye;
uniform vec4 GlobalAmbient;

out vec4 fColor;

void main()
{
    float deg = 0.017453292519943296;

    vec4 cc;
    cc = color;  // If no lighting, pass-through.

    if (Lt.on)  // Color has been replaced by Material Properties
    {
        vec3 n = normalize(normal);
        vec3 l = normalize(vec3(Lt.position)-vec3(position));
        vec3 r = normalize(2.0*dot(l,n)*n - l);
        vec3 v = normalize(eye-vec3(position));
        float lightDistance =length(vec3(Lt.position)-vec3(position));

        float dfang = max(0.0, dot(l, n));
        float specang = max(0.0, dot(r, v));
        if (dfang == 0)
            specang = 0;

        float attenuation = 1.0 / (Lt.attenuation[0] +
                                   Lt.attenuation[1] * lightDistance +
                                   Lt.attenuation[2] * lightDistance * lightDistance);

        float spotCos = dot(l, -normalize(Lt.spotDirection));
        float SpotCosCutoff = cos(Lt.spotCutoff*deg);  // assumes that spotCutoff is in degrees

        float spotFactor = 1.0;
        if (spotCos < SpotCosCutoff)
            spotFactor = 0.0;
        else if (Lt.spotCutoff < 179.9) // Only fade if a spotlight
            spotFactor = pow((spotCos+1)/2, Lt.spotExponent);

        vec4 globalAmbientPortion = Mat.ambient*GlobalAmbient;
        vec4 ambientPortion = Mat.ambient*Lt.ambient;
        vec4 diffusePortion = Mat.diffuse*Lt.diffuse*dfang*attenuation*spotFactor;
        vec4 specularPortion = Mat.specular*Lt.specular*pow(specang, Mat.shininess)*attenuation*spotFactor;

        vec4 c = ambientPortion + diffusePortion + specularPortion + globalAmbientPortion + Mat.emission;
        cc = min(c, vec4(1.0));
    }

    fColor = cc;
}
