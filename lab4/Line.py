from Determinant import orientation
from Point import Point
class Line:
    def __init__(self, start, end):
        if start.x > end.x:
            start, end = end, start

        self.start = start
        self.end = end

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

    def intersection_point(self, other):
        a1 = (self.end.x - self.start.x)/ (self.end.y - self.start.y)
        a2 = (other.end.x - other.start.x)/ (other.end.y - other.start.y)
        b1 = self.start.y - a1 * self.start.x
        b2 = other.start.y - a2 * other.start.x

        intersection_x = (b2 - b1)/(a1 - a2)
        intersection_y = a1 * intersection_x + b1

        return Point(intersection_x, intersection_y)



    def __repr__(self):
        return f"[{self.start}, {self.end}]"