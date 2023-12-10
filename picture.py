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
        with open(f"{directory}/screenshot{num_png_files}.png", "wb") as f:
            pixels = self.ctx.read_pixels()
            image = Image.frombytes("RGB", (self.app.width, self.app.height), pixels)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image.save(f, "PNG")
            print(f"Saved screenshot to {directory}/screenshot{num_png_files}.png")
        