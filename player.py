import pygame as pg
from camera import Camera
from settings import *

class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)
    
    def update(self):
        self.mouse_input()
        self.keyboard_input()
        super().update()

    def mouse_input(self):
        # Looks for inputs of mouse movement and rotate camera accordingly
        delta_x, delta_y = pg.mouse.get_rel()
        if delta_x: 
            self.rotate_yaw(delta_x=delta_x * MOUSE_SENSITIVITY)
        if delta_y:
            self.rotate_pitch(delta_y=delta_y * MOUSE_SENSITIVITY)

    def keyboard_input(self):
        # Looks for inputs of key presses and moves camera accordingly
        keys = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        # Moves player horizontally
        if keys[pg.K_w]:
            self.move_forward(vel)
        if keys[pg.K_s]:
            self.move_backward(vel)
        if keys[pg.K_a]:
            self.move_left(vel)
        if keys[pg.K_d]:
            self.move_right(vel)
        # Moves player vertically
        if keys[pg.K_SPACE]:
            self.move_up(vel)
        if keys[pg.K_LSHIFT]:
            self.move_down(vel)