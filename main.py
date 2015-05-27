#! /usr/bin/python3

import pygame

from app import App

if __name__ == "__main__":
    pygame.init()
    a = App()
    a.on_mainloop()
    pygame.quit()