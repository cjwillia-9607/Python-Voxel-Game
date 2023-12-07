from settings import *

class Camera:
    def __init__(self, position, yaw, pitch):

        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        # Relative directions
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.forward = glm.vec3(0.0, 0.0, -1.0)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, CAM_NEAR, CAM_FAR)
        self.m_view = glm.mat4()
    
    def update(self):
        self.update_vectors()
        self.udpate_view_matrix()

    def udpate_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        # Recalculate forward vector direction based on yaw and pitch
        self.forward.x = math.cos(self.yaw) * math.cos(self.pitch)
        self.forward.y = math.sin(self.pitch)
        self.forward.z = math.sin(self.yaw) * math.cos(self.pitch)
        self.forward = glm.normalize(self.forward)
        
        # Recalculate right and up
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0.0, 1.0, 0.0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        # Rotates the camera's pitch based on mouse movement in y-dir
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_LIMIT, PITCH_LIMIT)
    
    def rotate_yaw(self, delta_x):
        # Rotates the camera's yaw based on mouse movement in x-dir
        self.yaw += delta_x
    
    def move_forward(self, velocity):
        self.position += self.forward * velocity

    def move_right(self, velocity):
        self.position += self.right * velocity
    
    def move_up(self, velocity):
        self.position += self.up * velocity
    
    def move_down(self, velocity):
        self.position -= self.up * velocity
    
    def move_left(self, velocity):
        self.position -= self.right * velocity
    
    def move_backward(self, velocity):
        self.position -= self.forward * velocity