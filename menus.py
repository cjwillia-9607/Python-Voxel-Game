from settings import *
import pygame as pg

class Menu:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.screen = app.screen
        self.font = pg.font.SysFont("monospace", 32)

    def render(self):
        self.screen.fill(BG_COLOR)
        self.draw_text('Press SPACE to start', self.font, TEXT_COLOR, self.screen, WIN_RES[0] // 2, WIN_RES[1] // 2)

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)