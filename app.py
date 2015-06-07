#! /usr/bin/python3

from math import pi

import pygame
from pygame.locals import *

from ray_cast_engine import RayCastEngine, Player

from labyrinth import laby

from blocks import *

MAP = [
    [wall((0, 0, 255)), wall((0, 0, 255)), wall(
        (0, 255, 0)),  wall((0, 0, 255))],
    [wall((0, 0, 255)), EMPTY, EMPTY, wall((0, 0, 255))],
    [wall((0, 0, 255)), wall((0, 0, 255)), wall(
        (0, 0, 255)), wall((0, 0, 255))],
]


class App:

    def __init__(self):
        self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        pygame.mouse.set_visible(False)
        pygame.key.set_repeat(5, 5)
        self.player = Player((BLOCK_WIDTH * 1.5, BLOCK_WIDTH * 1.5), 277)
        self.engine = RayCastEngine(self.player, laby((30, 30)))
        self.running = True
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

    def on_event(self, e):
        if e.type == QUIT:
            self.running = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                self.running = False
            if e.key == K_q:
                self.player.turn_left(pi / 12)
            elif e.key == K_s:
                self.player.turn_right(pi / 12)
            elif e.key == K_a:
                self.player.dist_cam -= 5
                if self.player.dist_cam < 1:
                    self.player.dist_cam = 1
            elif e.key == K_z:
                self.player.dist_cam += 5
            elif e.key == K_LEFT:
                self.player.scroll_left(5)
            elif e.key == K_RIGHT:
                self.player.scroll_right(5)
            elif e.key == K_UP:
                self.player.forward(5)
            elif e.key == K_DOWN:
                self.player.backward(5)
            elif e.key == K_e:
                self.engine.column_width -= 1
                if self.engine.column_width <= 0:
                    self.engine.column_width = 1
            elif e.key == K_r:
                self.engine.column_width += 1
            elif e.key == K_f:
                self.engine.fish_eye = not self.engine.fish_eye

    def on_render(self):
        pygame.draw.rect(
            self.window, (0, 0, 0), (0, 0, self.window.get_width(), self.window.get_height()))
        self.engine.on_render(self.window)
        self.window.blit(self.font.render(
            "angle : " + str(self.player.angle), False, (255, 255, 255)), (0, 0))
        self.window.blit(self.font.render(
            "distance camera : " + str(self.player.dist_cam), False, (255, 255, 255)), (0, 30))
        self.window.blit(self.font.render(
            "position : " + str((int(self.player.x), int(self.player.y))), False, (255, 255, 255)), (0, 60))
        self.window.blit(self.font.render(
            "largeur colonne : " + str(self.engine.column_width) + " px", False, (255, 255, 255)), (0, 90))
        if self.engine.fish_eye:
            self.window.blit(self.font.render("Fish-eye activé", False, (255, 255, 255)), (0, 120))
        else:
            self.window.blit(self.font.render("Fish-eye désactivé", False, (255, 255, 255)), (0, 120))

    def on_mainloop(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            pygame.display.flip()
            # pygame.time.Clock().tick(20)
