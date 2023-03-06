import pygame
from config import *
from draw import Drawing
from record import Record
from controller import Controller

class Game:

    def __init__(self) -> None:
        pygame.init()
        self.sc = pygame.display.set_mode(RES)
        self.game_sc = pygame.Surface(GAME_RES)
        self.toolart = Drawing(self.sc, self.game_sc)
        self.controller = Controller()

    def get_actions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.controller.dx = -1
                elif event.key == pygame.K_RIGHT:
                    self.controller.dx = 1
                elif event.key == pygame.K_UP:
                    self.controller.need_rotate = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.controller.force_move_down()

    def take_actions(self):
        self.controller.move_x()
        self.controller.move_y()
        self.controller.rotate()
        self.controller.check_lines()
        self.controller.compute_score()
        self.toolart.draw_grid()
        self.toolart.draw_figure(self.controller.figure, self.controller.figure_rect, self.controller.color)
        self.toolart.draw_field(self.controller.field, self.controller.figure_rect)
        self.toolart.draw_next_figure(self.controller.figure_rect, self.controller.next_figure, self.controller.next_color)
        self.toolart.draw_titles(self.controller.score, self.controller.record)
        self.gameover()

    def gameover(self):
        for i in range(W):
            if self.controller.field[0][i]:
                Record().set(self.controller.record, self.controller.score)
                self.controller.field = [[0 for i in range(W)] for i in range(H)]
                self.controller.score = 0
                for i_rect in self.toolart.grid:
                    pygame.draw.rect(self.toolart.game_sc, get_color(), i_rect)
                    self.toolart.sc.blit(self.toolart.game_sc, (20, 20))
                    pygame.display.flip()
    
    def play(self):
        while True:
            self.controller.reset()
            self.toolart.draw_background()
            self.get_actions()
            self.take_actions()
            pygame.display.flip()


game = Game()
game.play()