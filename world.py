from settings import *
from world_objects.chunk import Chunk

class World:
    def __init__(self, app, seed):
        self.app = app
        self.seed = seed
        self.chunks = [None for _ in range(WORLD_VOL)]  # Initialize list for each chunk in world
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype=np.uint8)
        self.build_chunks()
        self.build_chunk_mesh()
    
    def build_chunks(self):
        # Iterate through the world and build each chunk in world
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position = (x, y, z), seed = self.seed)
                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk
                    # Build voxels for each chunk
                    self.voxels[chunk_index] = chunk.build_voxels()
                    # get pointer to voxel
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def render(self):
        for chunk in self.chunks:
            chunk.render()