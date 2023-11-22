import pygame
from Point import Point
from Polygon import Polygon
from Button import Button
from Saver import Saver
from Loader import Loader

BLACK = (0, 0, 0)

class App:
    def __init__(self, width = 900, height = 700):
        self.WIDTH = width
        self.HEIGHT = height
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Zadawanie Wielokątu")
        self.clock = pygame.time.Clock()
        self.isRunning = True
        self.points = []
        self.polygon = None

    def drawPolygon(self, polygon):
        self.window.fill((0, 0, 0))
        for i in range(len(polygon)):
            pygame.draw.circle(self.window, (255, 255, 255), (polygon[i].x, polygon[i].y), 8)
            pygame.draw.line(self.window, (255, 255, 255),(polygon[i].x, polygon[i].y),
                             (polygon[(i+1)%len(polygon)].x, polygon[(i+1)%len(polygon)].y))

        pygame.draw.circle(self.window, (0, 255, 100), (polygon[-1].x, polygon[-1].y), 8)

    def addPoint(self):
        mouse = pygame.mouse.get_pos()
        self.points.append(Point(mouse[0], mouse[1]))
        self.drawPolygon(self.points)

    def finishPolygon(self):
        self.polygon = Polygon(self.points)
        self.points = []

    def run(self):
        saveButton = Button(self.WIDTH - self.WIDTH//4, self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Zapisz")
        calcButton = Button(self.WIDTH - 2*(self.WIDTH//4), self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Oblicz")
        loadButton = Button(self.WIDTH - 3 * (self.WIDTH // 4), self.HEIGHT - 80, self.WIDTH // 4, 80, self.window,
                            "Załaduj")
        createButton = Button(0, self.HEIGHT - 80, self.WIDTH // 4, 80, self.window,
                            "Stwórz")

        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if saveButton.isClicked():
                            saver = Saver(100, 200, 700, 100, self.window)
                            saver.run()
                            self.finishPolygon()
                            print(saver.text)
                            print(self.polygon)
                            saver.save(self.polygon)
                            self.window.fill(BLACK)
                            self.polygon = None
                        elif calcButton.isClicked():
                            continue
                        elif loadButton.isClicked():
                            loader = Loader()
                            self.polygon = loader.load()
                            self.polygon = self.polygon.points
                        elif createButton.isClicked():
                            self.polygon = None
                            self.points = []
                            self.window.fill(BLACK)
                        else:
                            self.addPoint()

            if self.polygon is not None:
                self.drawPolygon(self.polygon)


            saveButton.draw()
            calcButton.draw()
            loadButton.draw()
            createButton.draw()
            pygame.display.flip()

        pygame.quit()