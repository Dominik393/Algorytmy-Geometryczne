import pygame

class Button:
    def __init__(self, x, y, width, height, screen, text=None):
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.window = screen
        self.text = text
        self.font = pygame.font.SysFont('arial', 30)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(self.window, (0, 200, 150), self.rect)
        pygame.draw.rect(self.window, (0, 255, 150), self.rect.scale_by(0.90, 0.8))
        if self.text:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.window.blit(text_surface, text_rect)

    def isClicked(self):
        mouse = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse[0], mouse[1])
