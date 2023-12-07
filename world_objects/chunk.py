from settings import * 
from meshes.chunk_mesh import ChunkMesh

class Chunk:
    def __init__(self, app):
        self.app = app
        self.voxels: np.array = self.build_voxels()
        self.mesh: ChunkMesh = None
        self.build_mesh()
    
    def build_mesh(self):
        self.mesh = ChunkMesh(self)
    
    def render(self):
        self.mesh.render()
    
    def build_voxels(self) -> np.array:
        #empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype=np.int8) # Voxel is a number from 0 to 255, where 0 means empty space
        
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[(x + CHUNK_SIZE * z + CHUNK_AREA * y)] = 1
        return voxels      