import math
import numpy as np
import glm
from numba import njit

#resolution
WIN_RES = glm.vec2(1280, 720)

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG) # vertical fov
H_FOV = 2 * math.atan(math.tan(V_FOV / 2) * ASPECT_RATIO) # horizontal fov
CAM_NEAR = 0.1
CAM_FAR = 2000
PITCH_LIMIT = glm.radians(89.0)

# player
PLAYER_SPEED = 0.005
PLAYER_ROTATION_SPEED = 0.003
PLAYER_POS = glm.vec3(0, 0, 1)
MOUSE_SENSITIVITY = 0.002

# colors
BG_COLOR = glm.vec3(0.1, 0.16, 0.25)