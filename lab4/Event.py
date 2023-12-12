class Event:
    def __init__(self, val, is_start, segment_id):
        self.val = val
        self.is_start = is_start
        self.id = segment_id

    def __lt__(self, other):
        return self.val < other.val

    def __le__(self, other):
        return self.val <= other.val

    def __eq__(self, other):
        return self.val == other.val

    def __gt__(self, other):
        return self.val > other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __hash__(self):
        return hash((self.val, self.is_start, self.id))

    def __repr__(self):
        napis = "S" if self.is_start else "K"
        return f"x={self.val} id={self.id} {napis}"