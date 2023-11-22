import Point
import math

def getAngle(a, b, c):
    return abs(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))

class Polygon:
    def __init__(self, points = None):
        if points is None:
            self.points = []
        else:
            self.points = points

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
        poczatkowy = []
        koncowy = []
        laczacy = []
        dzielacy = []
        prawidlowy = []

        for i in range(len(self.points)):
            #Obaj są poniżej
            if self.points[(i - 1)%len(self.points)].y > self.points[i] and self.points[(i + 1)%len(self.points)].y > self.points[i]:
                if getAngle(self.points[(i - 1)%len(self.points)], self.points[i], self.points[(i + 1)%len(self.points)]) > math.pi:
                    dzielacy.append(self.points[i])
                elif getAngle(self.points[(i - 1)%len(self.points)], self.points[i], self.points[(i + 1)%len(self.points)]) < math.pi:
                    poczatkowy.append(self.points[i])
                else:
                    prawidlowy.append(self.points[i])
            elif self.points[(i - 1)%len(self.points)].y < self.points[i] and self.points[(i + 1)%len(self.points)].y < self.points[i]:
                if getAngle(self.points[(i - 1)%len(self.points)], self.points[i], self.points[(i + 1)%len(self.points)]) > math.pi:
                    laczacy.append(self.points[i])
                elif getAngle(self.points[(i - 1)%len(self.points)], self.points[i], self.points[(i + 1)%len(self.points)]) < math.pi:
                    koncowy.append(self.points[i])
                else:
                    prawidlowy.append(self.points[i])
            else:
                prawidlowy.append(self.points[i])

        return poczatkowy, koncowy, laczacy, dzielacy, prawidlowy

    def __repr__(self):
        text = "["
        for point in self.points:
            text += f"({point.x}, {point.y}), "
        text = text[:-2] + "]"
        return text