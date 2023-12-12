import random

from Determinant import orientation
from Point import Point


class Line:
    def __init__(self, start, end):
        if start.x > end.x:
            start, end = end, start

        self.start = start
        self.end = end
        self.curr = start.y

    def does_intersect(self, other):
        o1 = orientation(self.start, self.end, other.start)
        o2 = orientation(self.start, self.end, other.end)
        o3 = orientation(other.start, other.end, self.start)
        o4 = orientation(other.start, other.end, self.end)

        def on_segment(p, q, r):
            if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
                    q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
                return True
            return False

        if (o1 != o2 and o3 != o4):
            return True

        if (o1 == 0 and on_segment(self.start, other.start, self.end)):
            return True

        if (o2 == 0 and on_segment(self.start, other.end, self.end)):
            return True

        if (o3 == 0 and on_segment(other.start, self.start, other.end)):
            return True

        if (o4 == 0 and on_segment(other.start, self.end, other.end)):
            return True

        return False

    def get_slope(self):
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def get_intercept(self):
        return self.start.y - self.get_slope() * self.start.x

    def intersection_point(self, other):
        a1 = self.get_slope()
        a2 = other.get_slope()
        b1 = self.get_intercept()
        b2 = other.get_intercept()

        intersection_x = (b2 - b1) / (a1 - a2)
        intersection_y = a1 * intersection_x + b1

        return Point(intersection_x, intersection_y)

    def __repr__(self):
        return f"[{self.start}, {self.end}]"


def generateRandomLines(amount, xMin, xMax, yMin, yMax):
    lines = []

    xEnd = [i for i in range(xMin, xMax)]
    yStart = 0
    yEnd = 0
    random.shuffle(xEnd)

    for i in range(amount):
        xStart = random.randint(xMin, xMax)
        yStart = random.randint(yMin, yMax)
        yEnd = random.randint(yMin, yMax)
        while yStart == yEnd:
            yEnd = random.randint(yMin, yMax)
        lines.append(Line(Point(xStart, yStart), Point(xEnd[i], yEnd)))

    return lines
