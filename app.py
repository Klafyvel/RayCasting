#! /usr/bin/python3

from math import pi

import pygame
from pygame.locals import *

from ray_cast_engine import RayCastEngine, Player

from blocks import *

MAP = [
    [ wall((0,0,255)), wall((0,0,255)), wall((0,255,0)),  wall((0,0,255))],
    [EMPTY, EMPTY, EMPTY, wall((0,0,255))],
    [EMPTY, EMPTY, EMPTY, wall((0,0,255))],
]

class App:
    def __init__(self):
        self.window = pygame.display.set_mode((600,600))
        pygame.key.set_repeat(20, 20)
        self.player = Player((96,160), 277)
        self.engine = RayCastEngine(self.player, MAP)
        self.running = True
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
    def on_event(self, e):
        if e.type == QUIT:
            self.running = False
        elif e.type == KEYDOWN:
            if e.key == K_q:
                self.player.angle = (self.player.angle + pi/12)%(2*pi)
            elif e.key == K_s:
                self.player.angle = (self.player.angle - pi/12)%(2*pi)
            elif e.key == K_a:
                self.player.dist_cam -=5
                if self.player.dist_cam < 1:
                    self.player.dist_cam = 1
            elif e.key == K_z:
                self.player.dist_cam += 5
            elif e.key == K_LEFT:
                self.player.x -=5
            elif e.key == K_RIGHT:
                self.player.x +=5
            elif e.key == K_UP:
                self.player.y +=5
            elif e.key == K_DOWN:
                self.player.y -=5

    def on_render(self):
        pygame.draw.rect(self.window, (0,0,0), (0,0,self.window.get_width(), self.window.get_height()))
        self.engine.on_render(self.window)
        self.window.blit(self.font.render("angle : " + str(self.player.angle), False, (255,255,255)), (0,0))
        self.window.blit(self.font.render("distance camera : " + str(self.player.dist_cam), False, (255,255,255)), (0,30))
        self.window.blit(self.font.render("position : " + str((self.player.x, self.player.y)), False, (255,255,255)), (0,60))

    def on_mainloop(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            pygame.display.flip()
            pygame.time.Clock().tick(20)
        print(self.player.angle)
       
