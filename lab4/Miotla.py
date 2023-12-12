from Event import *
from sortedcontainers import SortedSet
from queue import PriorityQueue

def find_intersections(lines):
    q = PriorityQueue()

    for i, line in enumerate(lines):
        q.put(Event(line.start.x, 1, i))
        q.put(Event(line.end.x, 0, i))


    active_segments = SortedSet([])
    intersections = []
    calculatedPairs = []


    while not q.empty():
        currEvent = q.get()

        if currEvent.is_start == 1:
            active_segments.add((lines[currEvent.id].curr, currEvent.id))
            curr = active_segments.index((lines[currEvent.id].curr, currEvent.id))

            # Sprawdza czy przecina się z sąsiadem pod nim
            if curr > 0:
                if lines[currEvent.id].does_intersect(lines[active_segments[curr-1][1]]):
                    if (min(currEvent.id,active_segments[curr-1][1]), max(currEvent.id,active_segments[curr-1][1])) in calculatedPairs:
                        pass
                    else:
                        intersections.append(lines[currEvent.id].intersection_point(lines[active_segments[curr-1][1]]))
                        calculatedPairs.append((min(currEvent.id,active_segments[curr-1][1]), max(currEvent.id,active_segments[curr-1][1])))

                        if lines[currEvent.id].start.y < lines[active_segments[curr-1][1]].start.y:
                            q.put(Event(intersections[-1].x, 2, (currEvent.id, active_segments[curr-1][1])))
                        else:
                            q.put(Event(intersections[-1].x, 2, (active_segments[curr-1][1], currEvent.id)))

            # Sprawdza czy przecina się z sąsiadem nad nim
            if curr < len(active_segments)-1:
                if lines[currEvent.id].does_intersect(lines[active_segments[curr+1][1]]):
                    if (min(currEvent.id, active_segments[curr+1][1]),
                                                max(currEvent.id, active_segments[curr+1][1])) in calculatedPairs:
                        pass
                    else:
                        intersections.append(lines[currEvent.id].intersection_point(lines[active_segments[curr+1][1]]))
                        calculatedPairs.append((min(currEvent.id, active_segments[curr+1][1]),
                                                max(currEvent.id, active_segments[curr+1][1])))

                        if lines[currEvent.id].start.y < lines[active_segments[curr+1][1]].start.y:
                            q.put(Event(intersections[-1].x, 2, (currEvent.id, active_segments[curr+1][1])))
                        else:
                            q.put(Event(intersections[-1].x, 2, (active_segments[curr+1][1], currEvent.id)))

        elif currEvent.is_start == 0:
            active_segments.discard((lines[currEvent.id].curr, currEvent.id))

        else:
            if (lines[currEvent.id[0]].curr, currEvent.id[0]) in active_segments:
                active_segments.discard((lines[currEvent.id[0]].curr, currEvent.id[0]))
                lines[currEvent.id[0]].curr = lines[currEvent.id[0]].get_slope() * (currEvent.val + 10**(-5)) + lines[currEvent.id[0]].get_intercept()
                q.put(Event(currEvent.val + 10**(-5), 1, currEvent.id[0]))

            if (lines[currEvent.id[1]].curr, currEvent.id[1]) in active_segments:
                active_segments.discard((lines[currEvent.id[1]].curr, currEvent.id[1]))
                lines[currEvent.id[1]].curr = lines[currEvent.id[1]].get_slope() * (currEvent.val + 10**(-5)) + lines[currEvent.id[1]].get_intercept()
                q.put(Event(currEvent.val + 10**(-5), 1, currEvent.id[1]))


    #Restat curr value for every line
    for i in range(len(lines)):
        lines[i].curr = lines[i].start.y


    return intersections
