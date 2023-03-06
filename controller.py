from copy import deepcopy
import pygame
from config import *
from field import new_field
from record import Record

class Controller:
    def __init__(self) -> None:
        self.score = 0
        self.record = Record().get()
        self.figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
        self.figure, self.next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
        self.color, self.next_color = get_color(), get_color()
        self.clock = pygame.time.Clock()
        self.field = new_field()
        self.dx = 0
        self.last_move_down, self.last_force_move_down = 0, 0
        self.need_rotate = False
        self.score, self.lines = 0, 0
        self.scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def reset(self):
        self.dx = 0
        self.dy = 0
        self.need_rotate = False

    def move_x(self):
        figure_old = deepcopy(self.figure)
        for i in range(4):
            self.figure[i].x += self.dx
            if not self.check_borders(i):
                self.figure = deepcopy(figure_old)
                break

    def move_y(self):
        ticks = pygame.time.get_ticks()
        if ticks < self.last_move_down + 1000:
            return
        self.last_move_down = ticks
        figure_old = deepcopy(self.figure)
        for i in range(4):
            self.figure[i].y += 1
            if not self.check_borders(i):
                for i in range(4):
                    self.field[figure_old[i].y][figure_old[i].x] = self.color
                self.figure, self.color = self.next_figure, self.next_color
                self.next_figure, self.next_color = deepcopy(choice(figures)), get_color()
                break
            
    def force_move_down(self):
        ticks = pygame.time.get_ticks()
        if ticks < self.last_force_move_down + 50:
            return
        self.last_force_move_down = ticks
        figure_old = deepcopy(self.figure)
        for i in range(4):
            self.figure[i].y += 1
            if not self.check_borders(i):
                for i in range(4):
                    self.field[figure_old[i].y][figure_old[i].x] = self.color
                self.figure, self.color = self.next_figure, self.next_color
                self.next_figure, self.next_color = deepcopy(choice(figures)), get_color()
                break

    def rotate(self):
        center = self.figure[0]
        figure_old = deepcopy(self.figure)
        if self.need_rotate:
            for i in range(4):
                x = self.figure[i].y - center.y
                y = self.figure[i].x - center.x
                self.figure[i].x = center.x - x
                self.figure[i].y = center.y + y
                if not self.check_borders(i):
                    self.figure = deepcopy(figure_old)
                    break
    
    def check_borders(self, i):
        if self.figure[i].x < 0 or self.figure[i].x > W - 1:
            return False
        elif self.figure[i].y > H - 1 or self.field[self.figure[i].y][self.figure[i].x]:
            return False
        return True
    
    def check_lines(self):
        self.line, self.lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if self.field[row][i]:
                    count += 1
                self.field[self.line][i] = self.field[row][i]
            if count < W:
                self.line -= 1
            else:
                self.lines += 1
    
    def compute_score(self):
        self.score += self.scores[self.lines]