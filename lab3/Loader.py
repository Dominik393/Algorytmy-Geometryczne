import pygame
import pickle

class Loader:
    def __init__(self):
        self.polygons = None

    def load(self, name):
        with open("Save.txt", "rb") as file:
            self.polygons = pickle.load(file)
            if name in self.polygons:
                print(self.polygons[name])
                return self.polygons[name][0]
            else:
                return None

