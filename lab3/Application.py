import pygame
from Point import Point
from Polygon import Polygon
from Button import Button
from Saver import Saver
from Loader import Loader
from InputWindow import InputWindow
from Determinant import det_3D_matrix

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
            pygame.draw.circle(self.window, WHITE, (self.points[i].x, self.points[i].y), 8)
            pygame.draw.line(self.window, WHITE,(self.points[i].x, self.points[i].y),
                             (self.points[(i+1)%len(self.points)].x, self.points[(i+1)%len(self.points)].y))

        pygame.draw.circle(self.window, (0, 255, 100), (self.points[-1].x, self.points[-1].y), 8)

    def drawPolygon(self):
        self.window.fill(BLACK)
        if not self.polygon.classified:
            for i in range(len(self.polygon.points)):
                pygame.draw.circle(self.window, WHITE, (self.polygon.points[i].x, self.polygon.points[i].y), 8)
                pygame.draw.line(self.window, WHITE,(self.polygon.points[i].x, self.polygon.points[i].y),
                                 (self.polygon.points[(i+1)%len(self.polygon.points)].x, self.polygon.points[(i+1)%len(self.polygon.points)].y), 2)

        else:
            for i in range(len(self.polygon.points)):
                pygame.draw.line(self.window, WHITE, (self.polygon.points[i].x, self.polygon.points[i].y),
                                 (self.polygon.points[(i + 1) % len(self.polygon.points)].x,
                                  self.polygon.points[(i + 1) % len(self.polygon.points)].y), 2)

            for point in self.polygon.points:
                if point.type == 'p':
                    pygame.draw.circle(self.window, (24, 237, 81), (point.x, point.y), 8)
                elif point.type == 'k':
                    pygame.draw.circle(self.window, (252, 18, 53), (point.x, point.y), 8)
                elif point.type == 'l':
                    pygame.draw.circle(self.window, (2, 7, 163), (point.x, point.y), 8)
                elif point.type == 'd':
                    pygame.draw.circle(self.window, (82, 183, 255), (point.x, point.y), 8)
                elif point.type == 'r':
                    pygame.draw.circle(self.window, (79, 52, 20), (point.x, point.y), 8)

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

    def finishPolygon(self):
        self.polygon = Polygon(self.points)
        self.points = []

    def classify(self):
        if self.polygon is None:
            return

        self.polygon.classify()

    def drawTriangulated(self, triangles):
        for triangle in triangles:
            for i in range(len(triangle)):
                pygame.draw.line(self.window, (255, 160, 160), (triangle[i].x, triangle[i].y),
                                 (triangle[(i + 1) % len(triangle)].x, triangle[(i + 1) % len(triangle)].y))


    def triangulationAnimation(self):
        _, chain = self.polygon.triangulate()
        stack = [chain[0], chain[1]]

        self.window.fill(BLACK)
        self.drawPolygon()
        pygame.display.flip()

        for i in range(2, len(chain)):
            curr = chain[i]

            for point in stack:
                pygame.draw.circle(self.window, (255, 255, 0), (point.x, point.y), 8)

            pygame.draw.circle(self.window, (255, 0, 0), (curr.x, curr.y), 8)
            pygame.display.flip()

            if curr.side != stack[-1].side:
                first = stack[-1]

                while stack:
                    vert = stack.pop()
                    if not self.polygon.doNeighbour(curr, vert):
                        pygame.draw.line(self.window, (255, 160, 160), (curr.x, curr.y),
                                         (vert.x, vert.y))
                        self.waitForButtonPress()
                        pygame.display.flip()

                stack.append(first)

            else:
                last = stack.pop()

                while stack:
                    vert = stack.pop()

                    if not self.polygon.doNeighbour(curr, vert):
                        if curr.side == 'right' and det_3D_matrix(last, curr, vert) > 0:
                            pygame.draw.line(self.window, (255, 160, 160), (curr.x, curr.y),
                                             (vert.x, vert.y))
                            self.waitForButtonPress()
                            pygame.display.flip()
                            last = vert
                        elif curr.side == 'left' and det_3D_matrix(last, curr, vert) < 0:
                            pygame.draw.line(self.window, (255, 160, 160), (curr.x, curr.y),
                                             (vert.x, vert.y))
                            self.waitForButtonPress()
                            pygame.display.flip()
                            last = vert
                        else:
                            break

                stack.append(vert)
                stack.append(last)
            stack.append(curr)



    def run(self):
        #Buttons
        saveButton = Button(self.WIDTH - self.WIDTH//4, self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Zapisz")
        calcButton = Button(self.WIDTH - 2*(self.WIDTH//4), self.HEIGHT-80, self.WIDTH//4, 80, self.window, "Oblicz")
        loadButton = Button(self.WIDTH - 3 * (self.WIDTH // 4), self.HEIGHT - 80, self.WIDTH // 4, 80, self.window,
                            "Załaduj")
        createButton = Button(0, self.HEIGHT - 80, self.WIDTH // 4, 80, self.window,
                            "Stwórz")

        #SideButtons
        clasiffyButton = Button(self.WIDTH - 1.5*(self.WIDTH//4), self.HEIGHT - 160, self.WIDTH // 4, 80, self.window,
                            "Klasyfikacja")
        trianButton = Button(self.WIDTH - 1.5*(self.WIDTH//4), self.HEIGHT - 240, self.WIDTH // 4, 80, self.window,
                            "Triangulacja")
        #Rest
        inWin = InputWindow(100, 200, 700, 100, self.window)
        showSideButtons = False
        allowToCreate = False
        triangles = None


        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #Zapisz
                        if saveButton.isClicked():
                            allowToCreate = False
                            saver = Saver()
                            self.finishPolygon()
                            inWin.run()
                            saver.save(self.polygon, inWin.text)
                            inWin.reset()
                            self.window.fill(BLACK)
                            self.polygon = None
                            showSideButtons = False

                        #Oblicz
                        elif calcButton.isClicked():
                            if self.polygon is None:
                                break
                            allowToCreate = False
                            showSideButtons = True
                            triangles = None

                        #Wczytaj
                        elif loadButton.isClicked():
                            loader = Loader()
                            inWin.run()
                            self.polygon = loader.load(inWin.text)
                            inWin.reset()
                            self.window.fill(BLACK)
                            triangles = None
                            allowToCreate = False
                            showSideButtons = False

                        #Stwórz
                        elif createButton.isClicked():
                            self.polygon = None
                            self.points = []
                            self.window.fill(BLACK)
                            triangles = None
                            allowToCreate = True
                            showSideButtons = False

                        #Triangulate
                        elif trianButton.isClicked() and showSideButtons:
                            allowToCreate = False
                            if self.polygon.yMonotonicity():
                                print("Wielokąt jest Y monotoniczny")
                                triangles, chain = self.polygon.triangulate()
                                self.triangulationAnimation()
                                showSideButtons = False
                            else:
                                print("Wielokąt nie jest Y monotoniczny \nNie można stworzyć triangulacji")


                        #Sklasyfikuj
                        elif clasiffyButton.isClicked() and showSideButtons:
                            allowToCreate = False
                            triangles = None
                            self.classify()

                        elif allowToCreate:
                            showSideButtons = False
                            triangles = None
                            self.addPoint()

                        else:
                            showSideButtons = False

            if self.polygon is not None:
                self.drawPolygon()

            if triangles is not None:
                self.drawPolygon()
                self.drawTriangulated(triangles)


            saveButton.draw()
            calcButton.draw()
            loadButton.draw()
            createButton.draw()
            if showSideButtons:
                clasiffyButton.draw()
                trianButton.draw()
            pygame.display.flip()

        pygame.quit()
