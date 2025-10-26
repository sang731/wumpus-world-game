import os
import pygame
from pygame import Surface
from config import ASSET_DIR

def load_image(name,size=None):
    path=os.path.join(ASSET_DIR,name)
    try:
        img=pygame.image.load(path).convert_alpha()
        if size:
            img=pygame.transform.smoothscale(img,size)
        return img
    except Exception:
        return None

def text_center(surface:Surface,rect,text,font,color):
    surf=font.render(text,True,color)
    surface.blit(surf,(rect.left+(rect.width-surf.get_width())/2,
                        rect.top+(rect.height-surf.get_height())/2))
