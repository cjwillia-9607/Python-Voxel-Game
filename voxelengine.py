from settings import *
import pygame as pg
import dearpygui.dearpygui as dpg
import sys
import moderngl as mgl
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures
from console import Console

class VoxelEngine:
    def __init__(self, seed):
        self.seed = seed
        # Initialize PyGame and OpenGL versions
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        # Initializes the PyGame display and creates OpenGL context (frame and depth buffers)
        self.window_surface = pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        pg.display.set_caption("Simple Voxel Engine")
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        # Enables automatic garbage collecting to clean up unused objects
        self.ctx.gc_mode = 'auto'

        # Initialize clock to keep track of program
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        # Locks mouse cursor to the application window
        self.mouse_lock = True
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # fonts
        self.font = pg.font.SysFont('Arial', 32)
        
        self.reset = False
        self.running = True
        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene  = Scene(self, self.seed)

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        # Displays frame rate
        pg.display.set_caption(f"Simple Voxel Engine | FPS: {self.clock.get_fps():.0f}")

    def render(self):
        # Clears any existing frame and depth buffers and create new scene and frame
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        pg.display.flip()

    def handle_events(self):
        # Watches for escape key presses to close window
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_t:
                # Unlocks or Locks mouse cursor to the application window
                if self.mouse_lock:
                    self.mouse_lock = False
                    pg.event.set_grab(False)
                    pg.mouse.set_visible(True)
                else:
                    self.mouse_lock = True
                    pg.event.set_grab(True)
                    pg.mouse.set_visible(False)
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.reset = True

    def run(self):
        while self.running:
            if self.reset:
                self.on_init()
                self.reset = False
            self.handle_events()
            self.update()
            self.render()
        
        pg.quit()
        sys.exit()
