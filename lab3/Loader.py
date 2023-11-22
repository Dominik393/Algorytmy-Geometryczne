import pygame
import pickle

class Loader:
    def __init__(self):
        self.polygon = None

    def load(self):
        with open("Save.txt", "rb") as file:
            self.polygon = pickle.load(file)
            print(self.polygon)
            return self.polygon

