from Event import *
from sortedcontainers import SortedSet

def find_intersections(lines):
    events = []

    for i, line in enumerate(lines):
        events.append(Event(line.start.x, True, i))
        events.append(Event(line.end.x, False, i))

    events = SortedSet(events)

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

