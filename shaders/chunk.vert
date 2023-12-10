#version 330 core

layout (location = 0) in ivec3 in_position;
layout (location = 1) in int voxel_id;
layout (location = 2) in int face_id;
layout (location = 3) in int amb_occ;
layout (location = 4) in int to_flip;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 voxel_color;
out vec2 uv;
out float shading;

const float amb_occ_vals[4] = float[4](0.1, 0.25, 0.5, 1.0);

const float face_shading[6] = float[6](
    1.0, 0.5,   // top/bot
    0.5, 0.8,   // right/left
    0.5, 0.8    // front/back
);

const vec2 uv_coords[4] = vec2[4](vec2(0, 0), vec2(0, 1),
                                  vec2(1, 0), vec2(1, 1));

// tex coord indicides for even then odd faces
const int uv_indices[24] = int[24](1, 0, 2, 1, 2, 3,    // tex_coords for even face
                                   3, 0, 2, 3, 1, 0,    // odd face
                                   3, 1, 0, 3, 0, 2,    // tex_coords for flipped even face
                                   1, 2, 3, 1, 0, 2);   // flipped odd

// hash function to map a number to a 3 component vector color
vec3 hash31(float p) {
    vec3 p_vec = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));
    p_vec += dot(p_vec, p_vec.yzx + 33.33);
    return fract((p_vec.xxy + p_vec.yzz) * p_vec.zyx) + 0.05;
}

void main() {
    int uv_index = gl_VertexID % 6  + ((face_id & 1) + to_flip * 2) * 6;    // Convert vertex id to uv
    uv = uv_coords[uv_indices[uv_index]];
    voxel_color = hash31(voxel_id);
    shading = face_shading[face_id] * amb_occ_vals[amb_occ];
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}