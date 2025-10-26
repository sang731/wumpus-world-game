from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MARGIN, HUD_HEIGHT, BG_COLOR, CELL_BORDER, CELL_COLOR, MAX_N, MIN_N, SENSORY_ACTIVE_BORDER,SENSORY_BG
from src.core.utils import load_image
from src.levels.generator import LevelGenerator
from src.entities.player import Player
from src.entities.wumpus import Wumpus
from src.entities.gold import Gold
from src.entities.pit import Pit
from src.entities.sensory import has_breeze, has_shine, has_stench
from src.ui.hud import HUD
from src.ui.popup import PopupManager

import pygame, sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wumpus World")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 18)
        self.big_font = pygame.font.SysFont(None, 28)

        self.n = self.ask_grid_size()
        self.difficulty = self.ask_difficulty()
        self.attempts_total = {'easy':3, 'medium':2, 'hard':1}[self.difficulty]
        self.attempts_left = self.attempts_total

        grid_w = SCREEN_WIDTH - 2*MARGIN
        grid_h = SCREEN_HEIGHT - HUD_HEIGHT - 2*MARGIN
        self.cell = min(grid_w, grid_h) // self.n

        gx = MARGIN
        gy = MARGIN
        self.grid_origin = (gx, gy)

        self.imgs = {}
        self.load_and_scale_images()

        self.level = LevelGenerator(self.n)
        self.player = Player(self.n, self.cell, self.grid_origin, self)

        if self.imgs.get("man.png"):
            self.player.set_image(self.imgs.get("man.png"))
        self.wumpus = Wumpus(self.level.wumpus)
        self.gold = Gold(self.level.gold)
        self.pits = [Pit(p) for p in self.level.pits]

        self.revealed = False
        self.game_over = False
        self.won = False

        self.hud = HUD(self)
        self.hud.set_arrow_icon(self.imgs.get("arrow.png"))
        self.popup = PopupManager(self)

    def ask_grid_size(self):
        while True:
            try:
                n = int(input(f"Enter grid size n (min {MIN_N}, max {MAX_N}): "))
                if MIN_N <= n <= MAX_N:
                    return n
                else:
                    print(f"Enter between {MIN_N} and {MAX_N}.")
            except Exception:
                print("Invalid input. Enter an integer.")

    def ask_difficulty(self):
        while True:
            v = input("Choose difficulty (easy / medium / hard): ").strip().lower()
            if v in ('easy','e'): return 'easy'
            if v in ('medium','m'): return 'medium'
            if v in ('hard','h'): return 'hard'
            print("Invalid selection.")

    def load_and_scale_images(self):
        size = (self.cell-6, self.cell-6)
        names = ['man.png','wumpus.png','gold.png','pit.png','breeze.png','shine.png','stench.png','arrow.png']
        for name in names:
            self.imgs[name] = load_image(name, size)

    def logical_to_screen(self, cell):
        gx,gy = self.grid_origin
        x,y = cell
        sx = gx + (x-1)*self.cell
        sy = gy + (self.n - y)*self.cell
        return sx,sy

    def draw_grid(self):
        gx,gy = self.grid_origin
        for i in range(self.n):
            for j in range(self.n):
                rect = pygame.Rect(gx + i*self.cell, gy + j*self.cell, self.cell, self.cell)
                pygame.draw.rect(self.screen, CELL_COLOR, rect)
                pygame.draw.rect(self.screen, CELL_BORDER, rect, 2)

    def draw_objects_revealed(self):
        if self.gold and (self.revealed or self.player.pos == self.gold.pos):
            self.draw_image_at(self.gold.pos, 'gold.png')

        if self.revealed and self.game_over and not self.won:
            for pit in self.pits:
                self.draw_image_at(pit.pos, 'pit.png')

        if self.revealed or not self.wumpus.alive:
            if self.wumpus.alive:
                self.draw_image_at(self.wumpus.pos, 'wumpus.png')
            else:
                self.draw_image_at(self.wumpus.pos, 'wumpus.png')
                sx,sy = self.logical_to_screen(self.wumpus.pos)
                rect = pygame.Rect(sx+3, sy+3, self.cell-6, self.cell-6)
                surf = self.big_font.render("X", True, (255,0,0))
                self.screen.blit(surf, (rect.centerx - surf.get_width()/2, rect.centery - surf.get_height()/2))

    def draw_image_at(self, cell, imgname):
        img = self.imgs.get(imgname)
        sx,sy = self.logical_to_screen(cell)
        rect = pygame.Rect(sx+3, sy+3, self.cell-6, self.cell-6)
        if img:
            self.screen.blit(img, rect)
        else:
            pygame.draw.rect(self.screen, (150,80,0), rect)
            f = pygame.font.SysFont(None, 14)
            self.screen.blit(f.render(imgname.split('.')[0].upper(), True, (0,0,0)), (rect.left+4, rect.top+4))

    def draw_sensory(self):
        x_offset = self.grid_origin[0] + self.n * self.cell + 12
        y_offset = self.grid_origin[1]
        y = y_offset
        
        pit_positions = set(pit.pos for pit in self.pits)
        
        sensory_indicators = [
            ('breeze.png', has_breeze(self.player.pos, pit_positions, self.n)),
            ('shine.png', has_shine(self.player.pos, self.gold.pos, self.n)),
            ('stench.png', has_stench(self.player.pos, self.wumpus.pos, self.wumpus.alive, self.n))
        ]
        
        for imgname, is_active in sensory_indicators:
            border_color = SENSORY_ACTIVE_BORDER if is_active else (255, 0, 0) 
            self.draw_small_icon(imgname, (x_offset, y), border_color)
            y += 120

    def draw_small_icon(self, imgname, pos, border_color=(100, 100, 120)):
        img = self.imgs.get(imgname)
        x, y = pos
        
        icon_size = 100
        border_size = 3
        total_size = icon_size + (border_size * 2)

        border_rect = pygame.Rect(x - border_size, y - border_size, total_size, total_size)
        pygame.draw.rect(self.screen, border_color, border_rect)
        
        inner_rect = pygame.Rect(x, y, icon_size, icon_size)
        pygame.draw.rect(self.screen,SENSORY_BG, inner_rect)
        
        if img:
            scaled_img = pygame.transform.smoothscale(img, (icon_size - 4, icon_size - 4))
            img_rect = scaled_img.get_rect(center=inner_rect.center)
            self.screen.blit(scaled_img, img_rect)
        else:
            pygame.draw.rect(self.screen, (200, 200, 200), inner_rect)
            f = pygame.font.SysFont(None, 14)
            text_surf = f.render(imgname.split('.')[0][:3].upper(), True, (0, 0, 0))
            text_x = x + (icon_size - text_surf.get_width()) // 2
            text_y = y + (icon_size - text_surf.get_height()) // 2
            self.screen.blit(text_surf, (text_x, text_y))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.draw_sensory()
        self.player.draw(self.screen)
        if self.player.pos == self.gold.pos:
            self.revealed = True
        self.draw_objects_revealed()
        
        self.hud.draw(self.screen)
        self.popup.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hud.icon_rect and self.hud.icon_rect.collidepoint(event.pos) and not self.game_over:
                    if self.player.arrows > 0:
                        self.player.arrow_mode = True
                    else:
                        self.popup.show("No arrows left")

            if event.type == pygame.KEYDOWN:
                if self.popup.popup_text:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        if self.won or self.attempts_left <= 0:
                            self.restart_game()
                        else:
                            self.popup.dismiss()
                    continue

                if event.key in (pygame.K_UP, pygame.K_w):
                    self.key_action((0,1))
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.key_action((0,-1))
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.key_action((-1,0))
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.key_action((1,0))
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

    def key_action(self, direction):
        if self.player.arrow_mode:
            self.fire_arrow(direction)
            self.player.arrow_mode = False
            return
        moved = self.player.move(direction[0], direction[1])

        if moved:
            px,py = self.player.pos

            if (px,py) in (p.pos for p in self.pits):
                self.player.points -= 1000
                self.attempts_left -= 1
                if self.attempts_left <= 0:
                    self.revealed = True
                    self.game_over = True
                    self.popup.show("You fell in a pit! No attempts left.. Press any key to restart.")
                else:
                    self.player.pos = (1,1)
                    self.popup.show(f"You fell in a pit...Attempts left: {self.attempts_left}")
                return

            if (px,py) == self.wumpus.pos and self.wumpus.alive:
                self.player.points -= 1000
                self.attempts_left -= 1
                if self.attempts_left <= 0:
                    self.revealed = True
                    self.game_over = True
                    self.popup.show("Wumpus ate you! No attempts left..Press any key to restart.")
                else:
                    self.player.pos = (1,1)
                    self.popup.show(f"Wumpus ate you...Attempts left: {self.attempts_left}")
                return

            if (px,py) == self.gold.pos:
                self.player.points=self.player.points+1000
                self.revealed = True
                self.game_over = True
                self.won = True
                self.popup.show("You found the gold! You win! Press any key to play again.")
                return

    def fire_arrow(self, direction):
        if self.player.arrows <= 0:
            self.popup.show("No arrows left")
            return
        self.player.arrows -= 1
        dx,dy = direction
        px,py = self.player.pos
        cx,cy = px+dx, py+dy
        hit = False
        while 1 <= cx <= self.n and 1 <= cy <= self.n:
            if (cx,cy) == self.wumpus.pos and self.wumpus.alive:
                hit = True
                break
            cx += dx; cy += dy
        if hit:
            self.wumpus.alive = False
            self.player.points += 100
            self.popup.show("You killed the Wumpus! +100 pts")
        else:
            self.player.points -= 10
            self.popup.show("Arrow missed. -10 pts")

    def update(self):
        if self.player.pos == self.gold.pos:
            self.player.points += 1000
            self.revealed = True
            self.game_over = True
            self.won = True
            self.popup.show("You found the gold! You win! Press any key to play again.")

    def restart_game(self):
        self.level = LevelGenerator(self.n)
        self.player = Player(self.n, self.cell, self.grid_origin, self)
        
        if self.imgs.get("man.png"):
            self.player.set_image(self.imgs.get("man.png"))
        self.wumpus = Wumpus(self.level.wumpus)
        self.gold = Gold(self.level.gold)
        self.pits = [Pit(p) for p in self.level.pits]
        
        self.revealed = False
        self.game_over = False
        self.won = False
        self.attempts_left = self.attempts_total  
        self.popup.dismiss()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)