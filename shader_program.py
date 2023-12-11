from settings import *

class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        # shaders
        self.chunk = self.get_program(shader_name='chunk')  # Creates shader program for chunk
        
        self.set_uniforms_on_init()


    def set_uniforms_on_init(self):
        # Sets uniform variables in vertex shader
        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['u_texture_0'] = 0

    def update(self):
        self.chunk['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        # Reads and loads vertex and frag shaders
        with open(f"shaders/{shader_name}.vert") as f:
            vertex_shader = f.read()
        with open(f"shaders/{shader_name}.frag") as f:
            fragment_shader = f.read()
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program