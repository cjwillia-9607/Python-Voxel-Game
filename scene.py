from settings import *
from meshes.quad_mesh import QuadMesh

class Scene:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        self.quad = QuadMesh(app)

    def update(self):
        pass

    def render(self):
        self.quad.render()