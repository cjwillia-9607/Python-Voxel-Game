from settings import *

class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.player = app.player

        # shaders
        self.quad = self.get_program(shader_name='quad')
        #
        self.set_uniforms_on_init()


    def set_uniforms_on_init(self):
        self.quad['m_proj'].write(self.player.m_proj)
        self.quad['m_model'].write(glm.mat4())

    def update(self):
        self.quad['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as f:
            vertex_shader = f.read()
        with open(f"shaders/{shader_name}.frag") as f:
            fragment_shader = f.read()
        return self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)