import pygame as pg
from camera import Camera
from settings import *
import glob
import os
import time

class Picture(Camera):
    # this class is a camera that is used to take a picture of the scene and save it to a file
    def __init__(self, app, position=glm.vec3(1.375*WORLD_W*CHUNK_SIZE,  11/3*WORLD_H*CHUNK_SIZE, 1.375*WORLD_W*CHUNK_SIZE), yaw=-132.20, pitch=-25.61):
        self.app = app
        self.ctx = self.app.ctx
        super().__init__(position, yaw, pitch)
        self.directory = "./screenshots/"
    
    def save(self, flag, ini_pos = None):
        # TODO: make it so that the picture is taken from this camera's POV, not player
        def count_png_files(directory):
            png_files = glob.glob(directory + "/*.png")
            return len(png_files)
        os.makedirs(self.directory, exist_ok=True)
        if flag:
            self.app.player.teleport(position = self.position, yaw=self.yaw, pitch=self.pitch)
            self.app.update()
            self.app.render()
            num_png_files = count_png_files(self.directory)
            fbo = self.app.ctx.screen
            pixel_data = fbo.read(components=3, dtype='f1')
            pixels = np.frombuffer(pixel_data, dtype=np.uint8)
            pixels = pixels.reshape((int(WIN_RES[1]), int(WIN_RES[0]), 3))[::-1, :, :]
            screenshot_surface = pg.surfarray.make_surface(pixels.swapaxes(1, 0))
            output_path = os.path.join(self.directory, f"screenshot{num_png_files}.png")
            pg.image.save(screenshot_surface, output_path)
        if not flag:
            self.app.player.teleport(position = self.position, yaw=self.yaw, pitch=self.pitch)
            self.app.update()
            self.app.render()
            num_png_files = count_png_files(self.directory) - 1
            fbo = self.app.ctx.screen
            pixel_data = fbo.read(components=3, dtype='f1')
            pixels = np.frombuffer(pixel_data, dtype=np.uint8)
            pixels = pixels.reshape((int(WIN_RES[1]), int(WIN_RES[0]), 3))[::-1, :, :]
            screenshot_surface = pg.surfarray.make_surface(pixels.swapaxes(1, 0))
            output_path = os.path.join(self.directory, f"screenshot{num_png_files}.png")
            pg.image.save(screenshot_surface, output_path)
            self.app.player.teleport(position=ini_pos[0], yaw=ini_pos[1], pitch=ini_pos[2])
            self.app.update()
            self.app.render()