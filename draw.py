import pygame
from config import *

class Drawing:
    def __init__(self, sc, game_sc) -> None:
        self.sc = sc
        self.game_sc = game_sc
        self.bg = pygame.image.load('img/bg.jpg').convert()
        self.game_bg = pygame.image.load('img/bg2.jpg').convert()
        self.main_font = pygame.font.Font('font/font.ttf', 65)
        self.font = pygame.font.Font('font/font.ttf', 45)
        self.title_tetris = self.main_font.render('TETRIS', True, pygame.Color('darkorange'))
        self.title_score = self.font.render('score:', True, pygame.Color('green'))
        self.title_record = self.font.render('record:', True, pygame.Color('purple'))

        self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

    def draw_background(self):
        self.sc.blit(self.bg, (0, 0))
        self.sc.blit(self.game_sc, (20, 20))
        self.game_sc.blit(self.game_bg, (0, 0))

    def draw_titles(self, score, record):
        self.sc.blit(self.title_tetris, (485, -10))
        self.sc.blit(self.title_score, (535, 780))
        self.sc.blit(self.font.render(str(score), True, pygame.Color('white')), (550, 840))
        self.sc.blit(self.title_record, (525, 650))
        self.sc.blit(self.font.render(record, True, pygame.Color('gold')), (550, 710))

    def draw_grid(self):
        [pygame.draw.rect(self.game_sc, (40, 40, 40), i_rect, 1) for i_rect in self.grid]
    
    def draw_figure(self, figure, figure_rect, color):
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(self.game_sc, color, figure_rect)
    
    def draw_field(self, field, figure_rect):
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(self.game_sc, col, figure_rect)
    
    def draw_next_figure(self, figure_rect, next_figure, next_color):
        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 380
            figure_rect.y = next_figure[i].y * TILE + 185
            pygame.draw.rect(self.sc, next_color, figure_rect)