#! /usr/bin/python3

import pygame

from ray_cast_engine import RayCastEngine

class App:
    def __init__(self):
        self.window = pygame.display.set_mode((0,0), FULLSCREEN)
    def on_event(self, e):
        pass
    def on_render(self):
        pass
    def on_mainloop(self):
        pass