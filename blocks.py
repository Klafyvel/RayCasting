#! /usr/bin/python3


EMPTY = (0,0)
wall = lambda c : (1,c) 

class Block:
    """A block is an ampty space."""
    def __init__(self, pos):
        self.x, self.y = pos
    def on_render(self, target):
        return EMPTY

class Wall(Block):
    """A wall is a block which is not empty :p"""
    def __init__(self, pos, color):
        super().__init__(pos)
        self.color = color:
    def on_render(self, target):
        return wall(self.color)

class Map:
    """A map contains blocks and walls."""
    def __init__(self):
        self.map = []
    def get_block(self, pos):
        x,y = pos
        return self.map[y][x]