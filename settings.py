import math
import numpy as np
import glm
from numba import njit

#resolution
WIN_RES = glm.vec2(1920, 1080)

# chunk
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_SIZE * CHUNK_SIZE * CHUNK_SIZE

# world
WORLD_W, WORLD_H = 8, 3     # How many chunks in each direction
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_W * WORLD_H * WORLD_D

# world center
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG) # vertical fov
H_FOV = 2 * math.atan(math.tan(V_FOV / 2) * ASPECT_RATIO) # horizontal fov
CAM_NEAR = 0.1
CAM_FAR = 2000
PITCH_LIMIT = glm.radians(89.0)

# player
PLAYER_SPEED = 0.1
PLAYER_ROTATION_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, WORLD_H * CHUNK_SIZE, CENTER_XZ) # Initial position of player
MOUSE_SENSITIVITY = 0.0015

# colors
BG_COLOR = glm.vec3(0.53, 0.81, 0.92)
TEXT_COLOR = glm.vec3(255,255,255)