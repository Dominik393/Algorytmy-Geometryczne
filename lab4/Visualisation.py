import pygame
from Point import *
from Event import *
from Line import *
from Miotla import find_intersections
from Button import *
from sortedcontainers import SortedSet

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

    def addPoint(self):
        mouse = pygame.mouse.get_pos()
        self.points.append(Point(mouse[0], self.HEIGHT - mouse[1]))
        self.drawCurrent()

    def addLine(self):
        self.lines.append(Line(self.points[-1], self.points[-2]))
        self.drawCurrent()

    def drawCurrent(self):
        self.window.fill(BLACK)
        for line in self.lines:
            pygame.draw.line(self.window, (110, 10, 150), (line.start.x, self.HEIGHT - line.start.y), (line.end.x, self.HEIGHT - line.end.y), 2)
        for point in self.points:
            pygame.draw.circle(self.window, (80, 10, 150), (point.x, self.HEIGHT - point.y), 8)

    def drawPoints(self, points, color):
        for point in points:
            pygame.draw.circle(self.window, color, (point.x, self.HEIGHT - point.y), 8)

    def generateRandom(self, amount):
        self.lines = generateRandomLines(amount, 0, self.WIDTH, 0, self.HEIGHT)
        self.points = []
        for line in self.lines:
            self.points.append(line.start)
            self.points.append(line.end)


    def awaitButtonPress(self):
        pressed = False
        while not pressed:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed = True
    def sweepAnimation(self):
        events = []

        for i, line in enumerate(self.lines):
            events.append(Event(line.start.x, True, i))
            events.append(Event(line.end.x, False, i))

        events.sort(key=lambda event: (event.val, not event.is_start))

        active_segments = SortedSet([])
        intersections = []

        for event in events:
            self.window.fill(BLACK)
            self.drawCurrent()
            if event.is_start:
                self.awaitButtonPress()
                active_segments.add((self.lines[event.id].start.y, event.id))
                curr = active_segments.index((self.lines[event.id].start.y, event.id))

                if curr > 0:
                    if self.lines[event.id].does_intersect(self.lines[active_segments[curr - 1][1]]):
                        intersections.append(self.lines[event.id].intersection_point(self.lines[active_segments[curr - 1][1]]))
                        self.drawPoints(intersections, (255, 0, 0))
                if curr < len(active_segments) - 1:
                    if self.lines[event.id].does_intersect(self.lines[active_segments[curr + 1][1]]):
                        intersections.append(self.lines[event.id].intersection_point(self.lines[active_segments[curr + 1][1]]))
                        self.drawPoints(intersections, (255, 0, 0))
                pygame.display.flip()

            else:
                active_segments.remove((self.lines[event.id].start.y, event.id))



    def run(self):
        started_line = False
        genButton = Button(self.WIDTH - self.WIDTH//4, self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Generuj")
        animButton = Button(self.WIDTH - 2*self.WIDTH//4, self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Animacja")

        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and genButton.isClicked():
                        self.generateRandom(8)
                        self.drawCurrent()
                    if event.button == 1 and animButton.isClicked():
                        self.sweepAnimation()
                    elif event.button == 1 and not started_line:
                        self.addPoint()
                        started_line = True
                    elif event.button == 1 and started_line:
                        self.addPoint()
                        self.addLine()
                        started_line = False
                    elif event.button == 3:
                        new_points = find_intersections(self.lines)
                        self.drawCurrent()
                        self.drawPoints(new_points, (255, 0, 0))

            genButton.draw()
            animButton.draw()
            pygame.display.flip()

        pygame.quit()

pygame.init()
apka = App()
apka.run()
