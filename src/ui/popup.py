from config import POPUP_BG, POPUP_BORDER, TEXT

from time import time
import pygame

class PopupManager:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 34)
        self.small = pygame.font.SysFont(None, 18)
        self.popup_text = None

    def show(self, text):
        self.popup_text = text

    def dismiss(self):
        self.popup_text = None

    def draw(self, surface):
        if not self.popup_text:
            return
        
        w, h = 750, 160
        rx = (surface.get_width() - w)//2
        ry = (surface.get_height() - h)//2

        rect = pygame.Rect(rx, ry, w, h)
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        surface.blit(overlay, (0,0))

        pygame.draw.rect(surface, POPUP_BG, rect)
        pygame.draw.rect(surface, POPUP_BORDER, rect, 3)

        txt = self.font.render(self.popup_text, True, TEXT)
        surface.blit(txt, (rect.left+20, rect.top+30))
     
        if self.game.won or self.game.attempts_left <= 0:
            instr_text = "Press Enter to restart.."
        else:
            instr_text = "Press Enter to continue.."
            
        instr = self.small.render(instr_text, True, (160,160,160))
        surface.blit(instr, (rect.left+20, rect.top+100))