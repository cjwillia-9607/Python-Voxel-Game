from settings import * 
from meshes.chunk_mesh import ChunkMesh

class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world  # Each chunk will be associated with a world and position in given world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: None
        self.mesh: ChunkMesh = None
        self.is_empty = True    # flag to ensure no empty chunks are rendered
    
    def get_model_matrix(self):
        # Model matrix for chunk
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model
    
    def set_uniform(self):
        # Sets uniform variable in vertex shader
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)
    
    def render(self):
        if not self.is_empty:   # Render if not empty chunk
            self.set_uniform()
            self.mesh.render()
    
    def build_voxels(self) -> np.array:
        # empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype=np.uint8) # Voxel is a number from 0 to 255, where 0 means empty space
        
        # simple terrain generation
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE  # Chunk position in world coordinates

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = x + cx # World coord of curr voxel
                wz = z + cz
                # Simplex noise to generate terrain elevation differences
                world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    voxels[(x + CHUNK_SIZE * z + CHUNK_AREA * y)] = wy + 1
        if np.any(voxels):  # Checks if no chunks are empty
            self.is_empty = False
        return voxels