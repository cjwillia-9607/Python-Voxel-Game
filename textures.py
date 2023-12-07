import pygame as pg
import moderngl as mgl

class Textures:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        # Load texture
        self.texture_0 = self.load('frame.png')

        # Assign texture unit (0)
        self.texture_0.use(location = 0)

    def load(self, file_name):
        # Load texture file from assets folder
        texture = pg.image.load(f'assets/{file_name}')
        # Flip horizontally
        texture = pg.transform.flip(texture, flip_x = True, flip_y = False)

        # Apply texture to OpenGL
        texture = self.ctx.texture(size = texture.get_size(),
                                   components = 4,
                                   data = pg.image.tostring(texture, 'RGBA', False))
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        return texture