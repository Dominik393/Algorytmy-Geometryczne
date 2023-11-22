import pygame
import pickle

class Saver:
    def __init__(self, x, y, width, height, screen):
        self.text = ""
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.font = pygame.font.SysFont('arial', 36)
        self.rect = pygame.Rect(x, y, width, height)
        self.window = screen

    def draw(self):
        pygame.draw.rect(self.window, (0, 255, 150), self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        self.window.blit(text_surface, text_rect)


    def save(self, polygon):
        with open("Save.txt", "wb") as file:
            pickle.dump(polygon, file)

    def run(self):
        isRunning = True
        self.window.fill((0, 0, 0))

        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        isRunning = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

            self.draw()
            pygame.display.flip()