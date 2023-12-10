from settings import *
from world import World

# Class that renders the scene
class Scene:
    def __init__(self, app, seed):
        self.app = app
        self.ctx = app.ctx
        self.seed = seed
        self.world = World(self.app, self.seed)

    def update(self):
        self.world.update()

    def render(self):
        self.world.render()