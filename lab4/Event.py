class Event:
    def __init__(self, x, is_start, segment_id):
        self.x = x
        self.is_start = is_start
        self.segment_id = segment_id

    def __lt__(self, other):
        return self.x < other.x

    def __le__(self, other):
        return self.x <= other.x

    def __eq__(self, other):
        return self.x == other.x

    def __gt__(self, other):
        return self.x > other.x

    def __ge__(self, other):
        return self.x >= other.x

    def __hash__(self):
        return hash((self.x, self.is_start, self.segment_id))

    def __repr__(self):
        napis = "startowy" if self.is_start else "koncowy"
        return f"x= {self.x} id= {self.segment_id} {napis}"