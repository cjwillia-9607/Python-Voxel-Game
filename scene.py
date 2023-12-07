from settings import *
from world_objects.chunk import Chunk

# Class that renders the scene
class Scene:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.chunk = Chunk(self.app)

    def update(self):
        pass

    def render(self):
        self.chunk.render()