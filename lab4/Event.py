class Event:
    def __init__(self, x, is_start, segment_id):
        self.x = x
        self.is_start = is_start
        self.segment_id = segment_id

    def __repr__(self):
        napis = "startowy" if self.is_start else "koncowy"
        return f"x= {self.x} id= {self.segment_id} {napis}"