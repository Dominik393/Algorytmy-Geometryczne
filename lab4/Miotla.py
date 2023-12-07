from Point import *
from Line import *
from Determinant import *
from Event import *


def find_intersections(lines):
    events = []

    for i, line in enumerate(lines):
        events.append(Event(line.start.x, True, i))
        events.append(Event(line.end.x, False, i))

    events.sort(key=lambda event: (event.x, not event.is_start))

    active_segments = set()
    intersections = []

    for event in events:
        if event.is_start:
            for active_segment in active_segments:
                if lines[event.segment_id].does_intersect(lines[active_segment]):
                    intersections.append(lines[event.segment_id].intersection_point(lines[active_segment]))
            active_segments.add(event.segment_id)
        else:
            active_segments.remove(event.segment_id)

    return intersections

# Przykładowe użycie:
lines = [
    Line(Point(1, 1), Point(4, 4)),
    Line(Point(1, 8), Point(2, 4)),
    Line(Point(2, 2), Point(5, 3)),
    Line(Point(3, 6), Point(5, 1)),
    Line(Point(-5,10), Point(5, 0))
]

intersection_points = find_intersections(lines)
print("Punkty przecięcia odcinków:", intersection_points)
