import Point
import math

def det_3D_matrix(a, b, c):
    positive = (a.x * b.y) + (a.y * c.x) + (b.x * c.y)
    negative = (b.y * c.x) + (a.x * c.y) + (a.y * b.x)

    return positive - negative
    # 0 - Na prostej
    # >0 - Nad prostą
    # <0 - Pod prostą

class Polygon:
    def __init__(self, points = None):
        if points is None:
            self.points = []
        else:
            self.points = points

        self.classified = False
        self.poczatkowy = []
        self.koncowy = []
        self.laczacy = []
        self.dzielacy = []
        self.prawidlowy = []

    def loadList(self, list):
        for point in list:
            self.points.append(Point.Point(point[0], point[1]))

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

    def __repr__(self):
        text = "["
        for point in self.points:
            text += f"({point.x}, {point.y}), "
        text = text[:-2] + "]"
        return text
