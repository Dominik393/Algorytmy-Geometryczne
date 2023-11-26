import Point
from Determinant import det_3D_matrix
import math

class Polygon:
    def __init__(self, points = None):
        if points is None:
            self.points = []
        else:
            self.points = points
            for i in range(len(points)):
                self.points[i].id = i

        self.classified = False
        self.poczatkowy = []
        self.koncowy = []
        self.laczacy = []
        self.dzielacy = []
        self.prawidlowy = []

    def loadList(self, list):
        for point in list:
            self.points.append(Point.Point(point[0], point[1]))
        for i in range(len(self.points)):
            self.points[i].id = i

    def doNeighbour(self, pointA, pointB):
        if abs(pointA.id - pointB.id) == 1:
            return True
        if pointA.id == 0 and pointB.id == len(self.points) - 1:
            return True
        if pointB.id == 0 and pointA.id == len(self.points) - 1:
            return True
        return False

    def yMonotonicity(self):
        lowestIndex = 0
        highestIndex = 0

        for i in range(len(self.points)):
            lowestIndex = lowestIndex if self.points[lowestIndex].y > self.points[i].y else i
            highestIndex = highestIndex if self.points[highestIndex].y < self.points[i].y else i

        start = lowestIndex
        end = highestIndex
        while start != end:
            if self.points[start].y >= self.points[(start + 1)%len(self.points)].y:
                start = (start+1)%len(self.points)
            else:
                return False

        start = highestIndex
        end = lowestIndex
        while start != end:
            if self.points[start].y <= self.points[(start + 1) % len(self.points)].y:
                start = (start + 1) % len(self.points)
            else:
                return False

        return True

    def classify(self):
        for i in range(len(self.points)):
            #Sąsiedzi są poniżej
            if self.points[(i - 1)%len(self.points)].y > self.points[i].y and self.points[(i + 1)%len(self.points)].y > self.points[i].y:
                if det_3D_matrix(self.points[(i - 1)%len(self.points)], self.points[i], self.points[(i + 1)%len(self.points)]) > 10**(-11):
                    self.dzielacy.append(self.points[i])
                    self.points[i].type = 'd'
                elif det_3D_matrix(self.points[(i - 1)%len(self.points)], self.points[i], self.points[(i + 1)%len(self.points)]) < -10**(-11):
                    self.poczatkowy.append(self.points[i])
                    self.points[i].type = 'p'
                else:
                    self.prawidlowy.append(self.points[i])
                    self.points[i].type = 'r'
            #Sąsiedzi są powyżej
            elif self.points[(i - 1)%len(self.points)].y < self.points[i].y and self.points[(i + 1)%len(self.points)].y < self.points[i].y:
                if det_3D_matrix(self.points[(i - 1)%len(self.points)], self.points[i], self.points[(i + 1)%len(self.points)]) > 10**(-11):
                    self.laczacy.append(self.points[i])
                    self.points[i].type = 'l'
                elif det_3D_matrix(self.points[(i - 1)%len(self.points)], self.points[i], self.points[(i + 1)%len(self.points)]) < -10**(-11):
                    self.koncowy.append(self.points[i])
                    self.points[i].type = 'k'
                else:
                    self.prawidlowy.append(self.points[i])
                    self.points[i].type = 'r'
            else:
                self.prawidlowy.append(self.points[i])
                self.points[i].type = 'r'

        self.classified = True

    def triangulate(self):
        if not self.yMonotonicity():
            return

        lowestIndex = 0
        highestIndex = 0
        leftChain = []
        rightChain = []

        for i in range(len(self.points)):
            lowestIndex = lowestIndex if self.points[lowestIndex].y > self.points[i].y else i
            highestIndex = highestIndex if self.points[highestIndex].y < self.points[i].y else i

        start = lowestIndex
        end = highestIndex
        while start != end:
            if self.points[start].y >= self.points[(start + 1) % len(self.points)].y:
                self.points[start].side = 'left'
                leftChain.append(self.points[start])
                start = (start + 1) % len(self.points)

        start = highestIndex
        end = lowestIndex
        while start != end:
            if self.points[start].y <= self.points[(start + 1) % len(self.points)].y:
                self.points[start].side = 'right'
                rightChain.append(self.points[start])
                start = (start + 1) % len(self.points)

        chain = self.points.copy()
        chain.sort(reverse=True, key=lambda x: x.y)
        # i, j = len(leftChain) - 1, len(rightChain) - 1
        # while i > -1 and j > -1:
        #     if leftChain[i].y < rightChain[j].y:
        #         chain.append(leftChain[i])
        #         i -= 1
        #     else:
        #         chain.append(rightChain[j])
        #         j -= 1
        # while i > -1:
        #     chain.append(leftChain[i])
        #     i -= 1
        # while j > -1:
        #     chain.append(rightChain[j])
        #     j -= 1

        stack = [chain[0], chain[1]]
        triangles = []

        # for i in range(2, len(chain)):
        #     while len(stack) > 1 and det_3D_matrix(stack[-2], stack[-1], chain[i]) > 0:
        #         triangles.append([stack[-2], stack[-1], chain[i]])
        #         stack.pop()
        #     stack.append(chain[i])

        for i in range(2, len(chain)):
            curr = chain[i]

            if curr.side != stack[-1].side:
                fist = stack[-1]

                while stack:
                    vert = stack.pop()
                    if not self.doNeighbour(curr, vert):
                        triangles.append([curr, vert])

                stack.append(fist)
                stack.append(curr)

            else:
                last = stack.pop()

                while stack:
                    vert = stack.pop()

                    if not self.doNeighbour(curr, vert):
                        if curr.side == 'right' and det_3D_matrix(last, curr, vert) > 0:
                            triangles.append([curr, vert])
                            last = vert
                        elif curr.side == 'left' and det_3D_matrix(last, curr, vert) < 0:
                            triangles.append([curr, vert])
                            last = vert
                        else:
                            break

                stack.append(vert)
                stack.append(last)
                stack.append(curr)


        return triangles, chain





    def __repr__(self):
        text = "["
        for point in self.points:
            text += f"({point.x}, {point.y}), "
        text = text[:-2] + "]"
        return text
