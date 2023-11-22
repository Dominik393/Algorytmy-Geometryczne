class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = None

    def __repr__(self):
        return f"({self.x}, {self.y})"