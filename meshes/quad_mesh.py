import numpy as np
from settings import *
from meshes.base_mesh import BaseMesh

class QuadMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader_program.quad

        self.vbo_format = "3f 3f"
        self.attrs = ("in_position", "in_color")
        self.vao = self.get_vao()
    
    def get_vertex_data(self) -> np.array:
        vertices = [
            (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), 
            (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0)
        ]

        colors = [
            (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
            (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0)
        ]

        vertex_data = np.hstack([vertices, colors], dtype=np.float32)
        return vertex_data