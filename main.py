from settings import *
import pygame as pg
import sys
import moderngl as mgl
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures

class VoxelEngine:
    def __init__(self):
        # Initialize PyGame and OpenGL versions
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        # Initializes the PyGame display and creates OpenGL context (frame and depth buffers)
        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        # Enables automatic garbage collecting to clean up unused objects
        self.ctx.gc_mode = 'auto'

        # Initialize clock to keep track of program
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        # Locks mouse cursor to the application window
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.running = True
        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene  = Scene(self)

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        # Displays frame rate
        pg.display.set_caption(f"Voxel Engine | FPS: {self.clock.get_fps():.2f}")

    def render(self):
        # Clears any existing frame and depth buffers and create new scene and frame
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        pg.display.flip()

    def handle_events(self):
        # Watches for key presses to close window
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    engine = VoxelEngine()
    engine.run()