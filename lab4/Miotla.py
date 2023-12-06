class Event:
    def __init__(self, x, is_start, segment_id):
        self.x = x
        self.is_start = is_start
        self.segment_id = segment_id

    def __repr__(self):
        napis = "startowy" if self.is_start else "koncowy"
        return f"x= {self.x} id= {self.segment_id} {napis}"

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # punkty są współliniowe
    return 1 if val > 0 else 2  # zwraca 1 dla ruchu w lewo, 2 dla ruchu w prawo

def on_segment(p, q, r):
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
        q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
    return False

def do_intersect(seg1, seg2):
    p1, q1 = seg1
    p2, q2 = seg2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2 and o3 != o4):
        return True

    if (o1 == 0 and on_segment(p1, p2, q1)):
        return True

    if (o2 == 0 and on_segment(p1, q2, q1)):
        return True

    if (o3 == 0 and on_segment(p2, p1, q2)):
        return True

    if (o4 == 0 and on_segment(p2, q1, q2)):
        return True

    return False

def find_intersections(segments):
    events = []

    for i, segment in enumerate(segments):
        start, end = segment
        if start[0] > end[0]:
            start, end = end, start  # zamień punkty, aby start miał mniejszą współrzędną x
        events.append(Event(start[0], True, i))
        events.append(Event(end[0], False, i))

    # Sortowanie zdarzeń według współrzędnych x
    events.sort(key=lambda event: (event.x, not event.is_start))

    active_segments = set()
    intersections = []

    for event in events:
        if event.is_start:
            for active_segment in active_segments:
                if do_intersect(segments[event.segment_id], segments[active_segment]):
                    seg1 = segments[event.segment_id]
                    seg2 = segments[active_segment]
                    p1, q1 = seg1
                    p2, q2 = seg2
                    # Obliczenie punktu przecięcia odcinków
                    x_intersect = ((p1[0] * q1[1] - p1[1] * q1[0]) * (p2[0] - q2[0]) - (p1[0] - q1[0]) * (p2[0] * q2[1] - p2[1] * q2[0])) / ((p1[0] - q1[0]) * (p2[1] - q2[1]) - (p1[1] - q1[1]) * (p2[0] - q2[0]))
                    y_intersect = ((p1[0] * q1[1] - p1[1] * q1[0]) * (p2[1] - q2[1]) - (p1[1] - q1[1]) * (p2[0] * q2[1] - p2[1] * q2[0])) / ((p1[0] - q1[0]) * (p2[1] - q2[1]) - (p1[1] - q1[1]) * (p2[0] - q2[0]))
                    intersections.append((x_intersect, y_intersect))
            active_segments.add(event.segment_id)
        else:
            active_segments.remove(event.segment_id)

    return intersections

# Przykładowe użycie:
segments = [
    [(1, 1), (4, 4)],
    [(1, 8), (2, 4)],
    [(2, 2), (5, 2)],
    [(3, 6), (5, 1)]
]

intersection_points = find_intersections(segments)
print("Punkty przecięcia odcinków:", intersection_points)
