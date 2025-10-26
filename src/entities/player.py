from config import SCREEN_WIDTH,SCREEN_HEIGHT,ASSET_DIR,MARGIN,HUD_HEIGHT
from src.core.utils import load_image

import pygame
from typing import Tuple

class Player:
    def __init__(self, n, cell_size, origin, game_state):
        self.n = n
        self.cell = cell_size
        self.origin = origin  
        self.pos = (1,1)
        self.arrows = 2
        self.points = 1000
        self.arrow_mode = False
        self.game_state = game_state  
        self.img =self.set_image(img=ASSET_DIR+'/man.png')

    def set_image(self, img):
        self.img = img

    def logical_to_screen(self, cell):
        gx, gy = self.origin
        x,y = cell
        sx = gx + (x-1)*self.cell
        sy = gy + (self.n - y)*self.cell
        return (sx, sy)

    def move(self, dx, dy):
        if self.arrow_mode:
            return
        x,y = self.pos
        nx,ny = x+dx, y+dy
        if 1 <= nx <= self.n and 1 <= ny <= self.n:
            self.pos = (nx,ny)
            self.points -= 1
            return True
        return False

    def draw(self, surface):
        sx,sy = self.logical_to_screen(self.pos)
        rect = pygame.Rect(sx+3, sy+3, self.cell-6, self.cell-6)
        if self.img:
            surface.blit(self.img, rect)
        else:
            pygame.draw.rect(surface, (80,160,220), rect)
            font = pygame.font.SysFont(None, 14)
            surface.blit(font.render("YOU", True, (0,0,0)), (rect.left+6, rect.top+6))
