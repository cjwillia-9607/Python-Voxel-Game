import pygame as pg
from camera import Camera
from settings import *
import glob
import os

class Picture(Camera):
    # this class is a camera that is used to take a picture of the scene and save it to a file
    def __init__(self, app, position=glm.vec3(1.375*WORLD_W*CHUNK_SIZE,  11/3*WORLD_H*CHUNK_SIZE, 1.375*WORLD_W*CHUNK_SIZE), yaw=-133.37, pitch=-46.42):
        self.app = app
        self.ctx = self.app.ctx
        super().__init__(position, yaw, pitch)
        self.directory = "./screenshots/"
    
    def save(self):
        def count_png_files(directory):
            png_files = glob.glob(directory + "/*.png")
            return len(png_files)
        os.makedirs(self.directory, exist_ok=True)
        num_png_files = count_png_files(self.directory)
        fbo = self.ctx.screen
        pixel_data = fbo.read(components=3, dtype='f1')
        pixels = np.frombuffer(pixel_data, dtype=np.uint8)
        pixels = pixels.reshape((int(WIN_RES[1]), int(WIN_RES[0]), 3))[::-1, :, :]
        screenshot_surface = pg.surfarray.make_surface(pixels.swapaxes(1, 0))
        output_path = os.path.join(self.directory, f"screenshot{num_png_files}.png")
        pg.image.save(screenshot_surface, output_path)
        