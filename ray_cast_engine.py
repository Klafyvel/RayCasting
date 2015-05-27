#! /usr/bin/python3

from math import sqrt

from blocks import *

norm = lambda x, y : sqrt(x**2 + y**2)

class RayCastEngine:
    def __init__(self, player, world, screen_size=(0,0)):
        self.world = world
        self.screen_width, self.screen_height = screen_size
        self.player = player
    def get_obstacle_in_direction(self, first_point, second_point):
        x1, y1 = first_point
        x2, y2 = second_point

        f = lambda t: ((x2 - x1) * t + x1, (y2 - y1) * t + y1)

        obstacle = False
        out_of_map = False
        t = 1 # f(1) = (x2, y2)
        step = 1 / norm(x2-x1, y2 - y1)

        while not obstacle and not out_of_map:
            x,y = f(t)
            i,j = x / BLOCK_WIDTH, y / BLOCK_HEIGHT
            if j >= len(self.world) or i >= len(self.world[j]):
                out_of_map = True
            elif self.world[j][i][0] is 1:
                obstacle = True
            t += step
        if out_of_map:
            return None
        else:
            return f(t)
    def calc_column_height(self, pos_column):
        x, y = self.player.pos
        x_col,y_co: = pos_column
        return norm(*self.player.camera_vector) / norm(x-x_col, y-y_col) * BLOCK_THICKNESS



class Player:
    def __init__(self, screen_size=(0,0), pos=(0,0)):
        self.screen_size = screen_size
        self.x, self.y = pos