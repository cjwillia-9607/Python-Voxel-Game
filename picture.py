import pygame as pg
from camera import Camera
from settings import *
import io
import glob
from PIL import Image

class Picture(Camera):
    # this class is a camera that is used to take a picture of the scene and save it to a file
    def __init__(self, app, position=glm.vec3(1.375*WORLD_W*CHUNK_SIZE,  11/3*WORLD_H*CHUNK_SIZE, 1.375*WORLD_W*CHUNK_SIZE), yaw=-133.37, pitch=-46.42):
        self.app = app
        self.ctx = self.app.ctx
        super().__init__(position, yaw, pitch)
    
    def save(self):
        def count_png_files(directory):
            png_files = glob.glob(directory + "/*.png")
            return len(png_files)

        directory = "screenshots"
        num_png_files = count_png_files(directory)
        fbo = self.ctx.simple_framebuffer((int(WIN_RES[0]), int(WIN_RES[1])))
        pixel_data = fbo.read(components=3, dtype='f1')
        pixels = np.frombuffer(pixel_data, dtype=np.uint8)
        print(pixels)
        pixels = pixels.reshape((int(WIN_RES[1]), int(WIN_RES[0]), 3))
        screenshot_surface = pg.surfarray.make_surface(pixels.swapaxes(0, 1))
        pg.image.save(screenshot_surface, "{directory}/screenshot{num_png_files}.png")
        print(f"Saved screenshot to {directory}/screenshot{num_png_files}.png")
        