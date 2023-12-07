import pygame
from Point import Point
from Line import Line
from Miotla import find_intersections

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class App:
    def __init__(self, width=900, height=700):
        self.WIDTH = width
        self.HEIGHT = height
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Przeciecia")
        self.clock = pygame.time.Clock()
        self.isRunning = True
        self.points = []
        self.lines = []

    def waitForButtonPress(self):
        pressed = False
        while not pressed:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed = True

    def addPoint(self):
        mouse = pygame.mouse.get_pos()
        self.points.append(Point(mouse[0], mouse[1]))
        self.drawCurrent()

    def addLine(self):
        self.lines.append(Line(self.points[-1], self.points[-2]))
        self.drawCurrent()

    def drawCurrent(self):
        for line in self.lines:
            pygame.draw.line(self.window, (110, 10, 150), (line.start.x, line.start.y), (line.end.x, line.end.y), 2)
        for point in self.points:
            pygame.draw.circle(self.window, (80, 10, 150), (point.x, point.y), 8)

    def drawPoints(self, points, color):
        for point in points:
            pygame.draw.circle(self.window, color, (point.x, point.y), 8)

    def convertLines(self):
        for i in range(len(self.lines)):
            self.lines[i].start.y = self.HEIGHT - self.lines[i].start.y
            self.lines[i].end.y = self.HEIGHT - self.lines[i].end.y

    def convertPoints(self, points):
        for i in range(len(points)):
            points[i].y = self.HEIGHT - points[i].y

    def run(self):
        started_line = False

        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not started_line:
                        self.addPoint()
                        started_line = True
                    elif event.button == 1 and started_line:
                        self.addPoint()
                        self.addLine()
                        started_line = False
                    elif event.button == 3:
                        self.convertLines()
                        new_points = find_intersections(self.lines)
                        #self.convertPoints(new_points)
                        self.drawPoints(new_points, (255, 0, 0))
                        self.convertLines()
                        self.drawCurrent()

            pygame.display.flip()

        pygame.quit()


apka = App()
apka.run()
