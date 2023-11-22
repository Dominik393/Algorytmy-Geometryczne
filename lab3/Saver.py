import pygame
import pickle

class Saver:
    def __init__(self):
        self.polygons = {}

    def save(self, polygon, name):
        try:
            with open("Save.txt", 'rb') as file:
                self.polygons = pickle.load(file)
        except EOFError:
            self.polygons = {}

        if name not in self.polygons:
            self.polygons[name] = []  # Initialize list if the key doesn't exist

        self.polygons[name].append(polygon)

        with open("Save.txt", "wb") as file:
            pickle.dump(self.polygons, file)
