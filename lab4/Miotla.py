from Event import *
from sortedcontainers import SortedSet
from queue import PriorityQueue

def find_intersections(lines):
    q = PriorityQueue()

    for i, line in enumerate(lines):
        q.put(Event(line.start.x, 1, (i,)))
        q.put(Event(line.end.x, 0, (i,)))


    active_segments = SortedSet([])
    intersections = []
    calculatedPairs = []


    while not q.empty():
        currEvent = q.get()

        if currEvent.is_start == 1:
            active_segments.add((lines[currEvent.id[0]].curr, currEvent.id))
            curr = active_segments.index((lines[currEvent.id[0]].curr, currEvent.id))

            # Sprawdza czy przecina się z sąsiadem pod nim
            if curr > 0:
                for neighbourId in active_segments[curr-1][1]:
                    if neighbourId == currEvent.id[0]:
                        continue
                    if lines[currEvent.id[0]].does_intersect(lines[neighbourId]):
                        if (min(currEvent.id[0], neighbourId), max(currEvent.id[0], neighbourId)) in calculatedPairs:
                            pass
                        else:
                            intersections.append(lines[currEvent.id[0]].intersection_point(lines[neighbourId]))
                            calculatedPairs.append((min(currEvent.id[0], neighbourId), max(currEvent.id[0], neighbourId)))

                            if lines[currEvent.id[0]].start.y < lines[neighbourId].start.y:
                                q.put(Event(intersections[-1].x, 2, (currEvent.id[0], neighbourId)))
                            else:
                                q.put(Event(intersections[-1].x, 2, (neighbourId, currEvent.id[0])))

            # Sprawdza czy przecina się z sąsiadem nad nim
            if curr < len(active_segments)-1:
                for neighbourId in active_segments[curr+1][1]:
                    if neighbourId == currEvent.id[0]:
                        continue
                    if lines[currEvent.id[0]].does_intersect(lines[neighbourId]):
                        if (min(currEvent.id[0], neighbourId),
                                                    max(currEvent.id[0], neighbourId)) in calculatedPairs:
                            pass
                        else:
                            intersections.append(lines[currEvent.id[0]].intersection_point(lines[neighbourId]))
                            calculatedPairs.append((min(currEvent.id[0], neighbourId),
                                                    max(currEvent.id[0], neighbourId)))

                            if lines[currEvent.id[0]].start.y < lines[neighbourId].start.y:
                                q.put(Event(intersections[-1].x, 2, (currEvent.id[0], neighbourId)))
                            else:
                                q.put(Event(intersections[-1].x, 2, (neighbourId, currEvent.id[0])))

        elif currEvent.is_start == 0:
            active_segments.discard((lines[currEvent.id[0]].curr, currEvent.id))

        else:
            #Wyrzucamy stare punkty
            active_segments.discard((lines[currEvent.id[0]].curr, (currEvent.id[0],)))
            active_segments.discard((lines[currEvent.id[1]].curr, (currEvent.id[1],)))

            # Po czym dodajemy nowy
            lines[currEvent.id[0]].curr = lines[currEvent.id[0]].get_slope() * currEvent.val + lines[currEvent.id[0]].get_intercept()
            lines[currEvent.id[1]].curr = lines[currEvent.id[1]].get_slope() * currEvent.val + lines[currEvent.id[1]].get_intercept()
            q.put(Event(currEvent.val, 1, currEvent.id))


    #Restat curr value for every line
    for i in range(len(lines)):
        lines[i].curr = lines[i].start.y


    return intersections
