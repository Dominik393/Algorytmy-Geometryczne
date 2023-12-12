from Event import *
from sortedcontainers import SortedSet

def find_intersections(lines):
    events = []

    for i, line in enumerate(lines):
        events.append(Event(line.start.x, 1, i))
        events.append(Event(line.end.x, 0, i))

    events = SortedSet(events)
    lastEvent = events[-1]

    active_segments = SortedSet([])
    intersections = []


    i = 0
    while events[i] != lastEvent:
        currEvent = events[i]

        if currEvent.is_start == 1:
            active_segments.add((lines[currEvent.id].start.y, currEvent.id))
            curr = active_segments.index((lines[currEvent.id].start.y, currEvent.id))

            if curr > 0:
                if lines[currEvent.id].does_intersect(lines[active_segments[curr-1][1]]):
                    intersections.append(lines[currEvent.id].intersection_point(lines[active_segments[curr-1][1]]))
                    if lines[currEvent.id].start.y < lines[active_segments[curr-1][1]].start.y:
                        events.add(Event(intersections[-1].x, 2, (currEvent.id, active_segments[curr-1][1])))
                    else:
                        events.add(Event(intersections[-1].x, 2, (active_segments[curr-1][1], currEvent.id)))
            if curr < len(active_segments)-1:
                if lines[currEvent.id].does_intersect(lines[active_segments[curr+1][1]]):
                    intersections.append(lines[currEvent.id].intersection_point(lines[active_segments[curr+1][1]]))
                    if lines[currEvent.id].start.y < lines[active_segments[curr+1][1]].start.y:
                        events.add(Event(intersections[-1].x, 2, (currEvent.id, active_segments[curr+1][1])))
                    else:
                        events.add(Event(intersections[-1].x, 2, (active_segments[curr+1][1], currEvent.id)))

        elif currEvent.is_start == 0:
            active_segments.discard((lines[currEvent.id].curr, currEvent.id))

        else:
            if (lines[currEvent.id[0]].curr, currEvent.id[0]) in active_segments:
                active_segments.discard((lines[currEvent.id[0]].curr, currEvent.id[0]))
                lines[currEvent.id[0]].curr = lines[currEvent.id[0]].get_slope() * (currEvent.val + 10**(-5)) + lines[currEvent.id[0]].get_intercept()
                active_segments.add((lines[currEvent.id[0]].curr, currEvent.id[0]))

            if (lines[currEvent.id[1]].curr, currEvent.id[1]) in active_segments:
                active_segments.discard((lines[currEvent.id[1]].curr, currEvent.id[1]))
                lines[currEvent.id[1]].curr = lines[currEvent.id[1]].get_slope() * (currEvent.val + 10**(-5)) + lines[currEvent.id[1]].get_intercept()
                active_segments.add((lines[currEvent.id[1]].curr, currEvent.id[1]))


        i += 1

    #Restat curr value for every line
    for i in range(len(lines)):
        lines[i].curr = lines[i].start.y


    return intersections
