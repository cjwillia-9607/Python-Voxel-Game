from settings import *

def is_void(voxel_pos, chunk_voxels):
    # Checks if voxel is void (empty space)
    x, y, z = voxel_pos
    if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
        if chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]:
            return False
    return True

def add_data(vertex_data, index, *vertices):
    # Adds attributes to vertex data array 
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index

def build_chunk_mesh(chunk_voxels, format_size):
    # Only adds data from voxel faces that are visible to camera to imporve performance
    # Max 3 visible faces per voxel, 2 triangles per face, 3 verticies per triangle = 18 verticies
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype = 'uint8')
    index = 0
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                #Ignore empty space
                if voxel_id == 0:
                    continue
                
                # The following functions check if there is empty space beyond the face, if so then add its data (visible)
                # top face
                if is_void((x, y + 1, z), chunk_voxels):
                    # Attributes for 4 verticies of face (x, y, z, voxel_id, face_id)
                    v0 = (x,     y + 1, z,     voxel_id, 0)
                    v1 = (x + 1, y + 1, z,     voxel_id, 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = (x,     y + 1, z + 1, voxel_id, 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)
                
                # bottom face
                if is_void((x, y - 1, z), chunk_voxels):
                    v0 = (x,     y, z,     voxel_id, 1)
                    v1 = (x + 1, y, z,     voxel_id, 1)
                    v2 = (x + 1, y, z + 1, voxel_id, 1)
                    v3 = (x,     y, z + 1, voxel_id, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)
                
                # right face
                if is_void((x + 1, y, z), chunk_voxels):
                    v0 = (x + 1, y,     z,     voxel_id, 2)
                    v1 = (x + 1, y + 1, z,     voxel_id, 2)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = (x + 1, y,     z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), chunk_voxels):
                    v0 = (x, y,     z,     voxel_id, 3)
                    v1 = (x, y + 1, z,     voxel_id, 3)
                    v2 = (x, y + 1, z + 1, voxel_id, 3)
                    v3 = (x, y,     z + 1, voxel_id, 3)
                    
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
                
                # back face
                if is_void((x, y, z - 1), chunk_voxels):
                    v0 = (x,     y,     z , voxel_id, 4)
                    v1 = (x,     y + 1, z , voxel_id, 4)
                    v2 = (x + 1, y + 1, z , voxel_id, 4)
                    v3 = (x + 1, y    , z , voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                
                # front face
                if is_void((x, y, z + 1), chunk_voxels):
                    v0 = (x,     y,     z + 1, voxel_id, 5)
                    v1 = (x,     y + 1, z + 1, voxel_id, 5)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = (x + 1, y,     z + 1, voxel_id, 5)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
    # Returns part of array that contains only vertex data
    return vertex_data[:index + 1]