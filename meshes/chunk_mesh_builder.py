from settings import *
from numba import uint8

# Uses numba compiler to speed up mesh building process
@njit
def to_numba_uint8(x, y, z, voxel_id, face_id):
    # Converts data to uint8 format for numba to save memory
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id)

@njit
def get_chunk_index(world_vox_pos):
    wx, wy, wz = world_vox_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
        return -1   # If chunk is outside of world, return -1
    return cx + WORLD_W * cz + WORLD_AREA * cy

@njit
def is_void(local_vox_pos, world_vox_pos, world_voxels):
    # # Checks if voxel is void (empty space)
    # x, y, z = voxel_pos
    # if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
    #     if chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]:
    #         return False
    # return True

    # Optimized version of above code that takes into account neighboring chunks
    chunk_index = get_chunk_index(world_vox_pos)
    if chunk_index == -1:
        return False
    chunk_voxels = world_voxels[chunk_index]
    x, y, z = local_vox_pos
    voxel_id = x % CHUNK_SIZE + CHUNK_SIZE * (z % CHUNK_SIZE) + CHUNK_AREA * (y % CHUNK_SIZE)
    return not chunk_voxels[voxel_id]   # If voxel is empty, return True

@njit
def add_data(vertex_data, index, *vertices):
    # Adds data to vertex data array 
    for vertex in vertices:
        for data in vertex:
            vertex_data[index] = data
            index += 1
    return index

@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels):
    # Only adds data from voxel faces that are visible to camera to imporve performance
    # Max 3 visible faces per voxel, 2 triangles per face, 3 verticies per triangle = 18 verticies
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype=np.uint8)
    index = 0
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                #Ignore empty space
                if voxel_id == 0:
                    continue
                # Gets chunk positions and then world positions of voxel
                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE
                # The following functions check if there is empty space beyond the face, if so then add its data (visible)
                # top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    # Attributes for 4 verticies of face (x, y, z, voxel_id, face_id)
                    v0 = to_numba_uint8(x,     y + 1, z,     voxel_id, 0)
                    v1 = to_numba_uint8(x + 1, y + 1, z,     voxel_id, 0)
                    v2 = to_numba_uint8(x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = to_numba_uint8(x,     y + 1, z + 1, voxel_id, 0)
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)
                
                # bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    v0 = to_numba_uint8(x,     y, z,     voxel_id, 1)
                    v1 = to_numba_uint8(x + 1, y, z,     voxel_id, 1)
                    v2 = to_numba_uint8(x + 1, y, z + 1, voxel_id, 1)
                    v3 = to_numba_uint8(x,     y, z + 1, voxel_id, 1)
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)
                
                # right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    v0 = to_numba_uint8(x + 1, y,     z,     voxel_id, 2)
                    v1 = to_numba_uint8(x + 1, y + 1, z,     voxel_id, 2)
                    v2 = to_numba_uint8(x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = to_numba_uint8(x + 1, y,     z + 1, voxel_id, 2)
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    v0 = to_numba_uint8(x, y,     z,     voxel_id, 3)
                    v1 = to_numba_uint8(x, y + 1, z,     voxel_id, 3)
                    v2 = to_numba_uint8(x, y + 1, z + 1, voxel_id, 3)
                    v3 = to_numba_uint8(x, y,     z + 1, voxel_id, 3)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    v0 = to_numba_uint8(x,     y,     z + 1, voxel_id, 5)
                    v1 = to_numba_uint8(x,     y + 1, z + 1, voxel_id, 5)
                    v2 = to_numba_uint8(x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = to_numba_uint8(x + 1, y,     z + 1, voxel_id, 5)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    v0 = to_numba_uint8(x,     y,     z , voxel_id, 4)
                    v1 = to_numba_uint8(x,     y + 1, z , voxel_id, 4)
                    v2 = to_numba_uint8(x + 1, y + 1, z , voxel_id, 4)
                    v3 = to_numba_uint8(x + 1, y    , z , voxel_id, 4)
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
    # Returns part of array that contains only vertex data
    return vertex_data[:index + 1]