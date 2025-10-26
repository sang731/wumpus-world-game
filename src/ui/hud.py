import pygame
from config import HUD_HEIGHT, TEXT, ACCENT
from src.core.utils import load_image

class HUD:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 18)
        self.bigfont = pygame.font.SysFont(None, 28)
        self.icon = None
        self.icon_rect = None

    def set_arrow_icon(self, img):
        self.icon = img

    def draw(self, surface):
        rtop = surface.get_height() - HUD_HEIGHT
        hud_rect = pygame.Rect(0, rtop, surface.get_width(), HUD_HEIGHT)
        pygame.draw.rect(surface, (18,18,22), hud_rect)
        pygame.draw.line(surface, (60,60,70), (0, rtop), (surface.get_width(), rtop), 2)

        surface.blit(self.font.render(f"Points: {self.game.player.points}", True, TEXT), (10, rtop+10))
        surface.blit(self.font.render(f"Arrows: {self.game.player.arrows}", True, TEXT), (10, rtop+35))
        surface.blit(self.font.render(f"Attempts Left: {self.game.attempts_left}", True, TEXT), (10, rtop+60))
        surface.blit(self.font.render("Click arrow icon then press a direction key to shoot", True, (170,170,170)), (200, rtop+10))

        ax = surface.get_width() - 110
        ay = rtop + 10
        self.icon_rect = pygame.Rect(ax, ay, 64, 64)
        pygame.draw.rect(surface, (40,40,50), self.icon_rect)
        pygame.draw.rect(surface, (90,90,100), self.icon_rect, 2)

        if self.icon:
            s = pygame.transform.smoothscale(self.icon, (56,56))
            surface.blit(s, (ax+4, ay+4))
        else:
            surface.blit(self.font.render("AR", True, TEXT), (ax+16, ay+20))

        if self.game.player.arrow_mode:
            pygame.draw.rect(surface, ACCENT, self.icon_rect, 3)