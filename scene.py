from settings import *
from world import World

# Class that renders the scene
class Scene:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.world = World(self.app)

    def update(self):
        self.world.update()

    def render(self):
        self.world.render()