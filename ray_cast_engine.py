#! /usr/bin/python3

from math import sqrt, cos, sin, modf

import pygame

from blocks import *

norm = lambda x, y: sqrt(x ** 2 + y ** 2)


class RayCastEngine:

    def __init__(self, player, world, floor=None, roof=None):
        self.world = world
        self.screen_width, self.screen_height = (0,0)
        self.player = player
        if floor:
            self.floor = pygame.image.load(floor).convert()
        else:
            self.floor = None
        if roof:
            self.roof = pygame.image.load(roof).convert()
        else:
            self.roof = None

    def get_obstacle_in_direction(self, first_point, second_point):
        x1, y1 = first_point
        x2, y2 = second_point

        f = lambda t: ((x2 - x1) * t + x1, (y2 - y1) * t + y1)

        obstacle = False
        out_of_map = False
        t = 0  # f(1) = (x2, y2)
        step = 1 / norm(x2 - x1, y2 - y1)
        x,y = 0,0
        while not obstacle and not out_of_map:
            x, y = f(t)
            i, j = int(modf(x / BLOCK_WIDTH)[1]), int(modf(y / BLOCK_HEIGHT)[1])
            if i < 0 or j < 0 or j >= len(self.world) or i >= len(self.world[j]):
                out_of_map = True
            elif self.world[j][i][0] is 1:
                obstacle = True
            t += step
        if out_of_map:
            return None
        else:
            return x,y

    def calc_column_height(self, pos_column):
        x, y = self.player.x, self.player.y
        x_col, y_col = pos_column
        return norm(*self.player.camera_vector()) / norm(x - x_col, y - y_col) * BLOCK_THICKNESS

    def create_screen_func(self):
        x,y = self.player.x, self.player.y
        x_cam,y_cam = self.player.camera_vector()
        n_x, n_y = y_cam, -x_cam
        return lambda t: (n_x * t + x + x_cam - n_x/2, n_y * t + y + y_cam - n_y/2)

    def on_render(self, target):
        if self.roof:
            target.blit(
                self.roof, (0, 0), area=(target.width(), target.height() / 2))
        if self.floor:
            target.blit(self.floor, (0, target.height() / 2),
                        area=(target.width(), target.height() / 2))
        self.screen_width, self.screen_height = 320,200
        f = self.create_screen_func()
        print(self.screen_width)
        for k in range(self.screen_width):
            x_cam, y_cam = f(k)
            p = self.get_obstacle_in_direction(
                (self.player.x,self.player.y), (x_cam, y_cam))
            if p:
                x,y = p
                i, j = int(modf(x / BLOCK_WIDTH)[1]), int(modf(y / BLOCK_HEIGHT)[1])
                height = self.calc_column_height((x, y))
    
                pygame.draw.rect(target, self.world[j][i][1],
                    (k+self.screen_width/2, (self.screen_height - height) / 2, 1, height))


class Player:

    def __init__(self, pos=(0, 0), dist_cam=1, angle=0):
        self.x, self.y = pos
        self.dist_cam=dist_cam
        self.angle = angle
    def camera_vector(self):
        return (cos(self.angle)*self.dist_cam , sin(self.angle)*self.dist_cam)
        # return (0,33)