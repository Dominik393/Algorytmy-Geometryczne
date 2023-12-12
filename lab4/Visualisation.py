import pygame
from Point import *
from Event import *
from Line import *
from Miotla import find_intersections
from Button import *
from sortedcontainers import SortedSet
from queue import PriorityQueue

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
        q = PriorityQueue()

        for i, line in enumerate(self.lines):
            q.put(Event(line.start.x, 1, i))
            q.put(Event(line.end.x, 0, i))

        active_segments = SortedSet([])
        intersections = []
        calculatedPairs = []

        while not q.empty():
            currEvent = q.get()

            if currEvent.is_start == 1:
                active_segments.add((self.lines[currEvent.id].curr, currEvent.id))
                curr = active_segments.index((self.lines[currEvent.id].curr, currEvent.id))

                # Sprawdza czy przecina się z sąsiadem pod nim
                if curr > 0:
                    if self.lines[currEvent.id].does_intersect(self.lines[active_segments[curr - 1][1]]):
                        if (min(currEvent.id, active_segments[curr - 1][1]),
                            max(currEvent.id, active_segments[curr - 1][1])) in calculatedPairs:
                            pass
                        else:
                            intersections.append(
                                self.lines[currEvent.id].intersection_point(self.lines[active_segments[curr - 1][1]]))
                            calculatedPairs.append((min(currEvent.id, active_segments[curr - 1][1]),
                                                    max(currEvent.id, active_segments[curr - 1][1])))

                            if self.lines[currEvent.id].start.y < self.lines[active_segments[curr - 1][1]].start.y:
                                q.put(Event(intersections[-1].x, 2, (currEvent.id, active_segments[curr - 1][1])))
                            else:
                                q.put(Event(intersections[-1].x, 2, (active_segments[curr - 1][1], currEvent.id)))

                # Sprawdza czy przecina się z sąsiadem nad nim
                if curr < len(active_segments) - 1:
                    if self.lines[currEvent.id].does_intersect(self.lines[active_segments[curr + 1][1]]):
                        if (min(currEvent.id, active_segments[curr + 1][1]),
                            max(currEvent.id, active_segments[curr + 1][1])) in calculatedPairs:
                            pass
                        else:
                            intersections.append(
                                self.lines[currEvent.id].intersection_point(self.lines[active_segments[curr + 1][1]]))
                            calculatedPairs.append((min(currEvent.id, active_segments[curr + 1][1]),
                                                    max(currEvent.id, active_segments[curr + 1][1])))

                            if self.lines[currEvent.id].start.y < self.lines[active_segments[curr + 1][1]].start.y:
                                q.put(Event(intersections[-1].x, 2, (currEvent.id, active_segments[curr + 1][1])))
                            else:
                                q.put(Event(intersections[-1].x, 2, (active_segments[curr + 1][1], currEvent.id)))

            elif currEvent.is_start == 0:
                active_segments.discard((self.lines[currEvent.id].curr, currEvent.id))

            else:
                if (self.lines[currEvent.id[0]].curr, currEvent.id[0]) in active_segments:
                    active_segments.discard((self.lines[currEvent.id[0]].curr, currEvent.id[0]))
                    self.lines[currEvent.id[0]].curr = self.lines[currEvent.id[0]].get_slope() * (currEvent.val + 10 ** (-5)) + \
                                                  self.lines[currEvent.id[0]].get_intercept()
                    q.put(Event(currEvent.val + 10 ** (-5), 1, currEvent.id[0]))

                if (self.lines[currEvent.id[1]].curr, currEvent.id[1]) in active_segments:
                    active_segments.discard((self.lines[currEvent.id[1]].curr, currEvent.id[1]))
                    self.lines[currEvent.id[1]].curr = self.lines[currEvent.id[1]].get_slope() * (currEvent.val + 10 ** (-5)) + \
                                                  self.lines[currEvent.id[1]].get_intercept()
                    q.put(Event(currEvent.val + 10 ** (-5), 1, currEvent.id[1]))

        # Restat curr value for every line
        for i in range(len(self.lines)):
            self.lines[i].curr = self.lines[i].start.y



    def run(self):
        started_line = False
        genButton = Button(self.WIDTH - self.WIDTH//4, self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Generuj")
        animButton = Button(self.WIDTH - 2*self.WIDTH//4, self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Animacja")
        clearButton = Button(self.WIDTH - 3*self.WIDTH//4, self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Wyczyść")

        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and genButton.isClicked():
                        self.generateRandom(5)
                        self.drawCurrent()
                    elif event.button == 1 and animButton.isClicked():
                        self.sweepAnimation()
                    elif event.button == 1 and clearButton.isClicked():
                        self.lines = []
                        self.points = []
                        self.drawCurrent()
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
            clearButton.draw()
            pygame.display.flip()

        pygame.quit()

pygame.init()
apka = App()
apka.run()
