import pygame

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = None
        self.type = None
        self.side = None

    def __repr__(self):
        return f"({self.x}, {self.y})"

