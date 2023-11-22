import pygame
from Point import Point
from Polygon import Polygon
from Button import Button
from Saver import Saver
from Loader import Loader
from InputWindow import InputWindow

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

    def drawCurrent(self):
        self.window.fill(BLACK)
        for i in range(len(self.points)):
            pygame.draw.circle(self.window, (255, 255, 255), (self.points[i].x, self.points[i].y), 8)
            pygame.draw.line(self.window, (255, 255, 255),(self.points[i].x, self.points[i].y),
                             (self.points[(i+1)%len(self.points)].x, self.points[(i+1)%len(self.points)].y))

        pygame.draw.circle(self.window, (0, 255, 100), (self.points[-1].x, self.points[-1].y), 8)

    def drawPolygon(self):
        if not self.polygon.classified:
            self.window.fill(BLACK)
            for i in range(len(self.polygon.points)):
                pygame.draw.circle(self.window, (255, 255, 255), (self.polygon.points[i].x, self.polygon.points[i].y), 8)
                pygame.draw.line(self.window, (255, 255, 255),(self.polygon.points[i].x, self.polygon.points[i].y),
                                 (self.polygon.points[(i+1)%len(self.polygon.points)].x, self.polygon.points[(i+1)%len(self.polygon.points)].y))

        else:
            self.window.fill(BLACK)
            for i in range(len(self.polygon.points)):
                pygame.draw.line(self.window, (255, 255, 255), (self.polygon.points[i].x, self.polygon.points[i].y),
                                 (self.polygon.points[(i + 1) % len(self.polygon.points)].x,
                                  self.polygon.points[(i + 1) % len(self.polygon.points)].y))
            for point in self.polygon.poczatkowy:
                pygame.draw.circle(self.window, (24, 237, 81), (point.x, point.y), 8)

            for point in self.polygon.koncowy:
                pygame.draw.circle(self.window, (252, 18, 53), (point.x, point.y), 8)

            for point in self.polygon.laczacy:
                pygame.draw.circle(self.window, (2, 7, 163), (point.x, point.y), 8)

            for point in self.polygon.dzielacy:
                pygame.draw.circle(self.window, (82, 183, 255), (point.x, point.y), 8)

            for point in self.polygon.prawidlowy:
                pygame.draw.circle(self.window, (79, 52, 20), (point.x, point.y), 8)

    def addPoint(self):
        mouse = pygame.mouse.get_pos()
        self.points.append(Point(mouse[0], mouse[1]))
        self.drawCurrent()

    def finishPolygon(self):
        self.polygon = Polygon(self.points)
        self.points = []

    def classify(self):
        if self.polygon is None:
            return

        self.polygon.classify()


    def run(self):
        saveButton = Button(self.WIDTH - self.WIDTH//4, self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Zapisz")
        calcButton = Button(self.WIDTH - 2*(self.WIDTH//4), self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Oblicz")
        loadButton = Button(self.WIDTH - 3 * (self.WIDTH // 4), self.HEIGHT - 80, self.WIDTH // 4, 80, self.window,
                            "Załaduj")
        createButton = Button(0, self.HEIGHT - 80, self.WIDTH // 4, 80, self.window,
                            "Stwórz")
        inWin = InputWindow(100, 200, 700, 100, self.window)


        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if saveButton.isClicked():
                            saver = Saver()
                            self.finishPolygon()
                            inWin.run()
                            saver.save(self.polygon, inWin.text)
                            inWin.reset()
                            self.window.fill(BLACK)
                            self.polygon = None
                        elif calcButton.isClicked():
                            self.classify()
                        elif loadButton.isClicked():
                            loader = Loader()
                            inWin.run()
                            self.polygon = loader.load(inWin.text)
                            inWin.reset()
                            self.window.fill(BLACK)
                        elif createButton.isClicked():
                            self.polygon = None
                            self.points = []
                            self.window.fill(BLACK)
                        else:
                            self.addPoint()

            if self.polygon is not None:
                self.drawPolygon()


            saveButton.draw()
            calcButton.draw()
            loadButton.draw()
            createButton.draw()
            pygame.display.flip()

        pygame.quit()