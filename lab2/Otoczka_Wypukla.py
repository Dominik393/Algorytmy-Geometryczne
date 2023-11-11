import math
import random
import time

import matplotlib.pyplot as plt


def generate_points(amount, Xrang, Yrang):
    points = []

    for i in range(amount):
        x = random.uniform(Xrang[0], Xrang[1])
        y = random.uniform(Yrang[0], Yrang[1])
        points.append((x,y))

    return points

def generate_circle_points(amount, radius, center = (0,0)):
    points = []

    for i in range(amount):
        angle = random.uniform(0, 2*math.pi)
        x = math.cos(angle) * radius + center[0]
        y = math.sin(angle) * radius + center[1]
        points.append((x,y))

    return points

def generate_rectangle_points(amount, lowerleft, upperright):
    points = []

    for i in range(amount):
        side = random.randint(0,3)

        if side == 0:   # Dolny Bok
            x = random.uniform(lowerleft[0], upperright[0])
            y = lowerleft[1]
            points.append((x,y))
        elif side == 1: # Prawy Bok
            x = upperright[0]
            y = random.uniform(lowerleft[1], upperright[1])
            points.append((x,y))
        elif side == 2: # Górny Bok
            x = random.uniform(lowerleft[0], upperright[0])
            y = upperright[1]
            points.append((x, y))
        else:           # Lewy Bok
            x = lowerleft[0]
            y = random.uniform(lowerleft[1], upperright[1])
            points.append((x,y))

    return points

def generate_square_points(amount_per_side, amount_per_diagonal, lowerleft, length):
    points = []

    for i in range(amount_per_side):
        x = random.uniform(lowerleft[0], lowerleft[0] + length)
        y = lowerleft[1]
        points.append((x,y))
        x = lowerleft[0]
        y = random.uniform(lowerleft[1], lowerleft[1] + length)
        points.append((x,y))

    for i in range(amount_per_diagonal):
        x1, x2 = random.uniform(lowerleft[0], lowerleft[0] + length), random.uniform(lowerleft[0], lowerleft[0] + length)
        b = lowerleft[1] - lowerleft[0]
        y1, y2 = b - x1 + length, b + x2
        points.append((x1,y1))
        points.append((x2,y2))

    return points

def det_3D_matrix(point, line):
    point = [point[0], point[1]]
    line[0] = [line[0][0], line[0][1]]
    line[1] = [line[1][0], line[1][1]]

    positive = (line[0][0] * line[1][1]) + (line[0][1] * point[0]) + (line[1][0] * point[1])
    negative = (line[1][1] * point[0]) + (line[0][0] * point[1]) + (line[0][1] * line[1][0])

    return positive - negative

def to_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def square_dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def Graham(points, epsilon = 0):
    if len(points) < 3:
        raise ValueError("Graham Scan requires at least 3 points")

    pivot = min(points, key=lambda p: (p[1], p[0]))

    sorted_points = sorted(points, key=lambda p: (to_angle(pivot, p), -square_dist(pivot, p)))
    sorted_points.remove(pivot)

    i = 0
    while i < len(sorted_points) - 1:
        if -epsilon <= det_3D_matrix(pivot, [sorted_points[i], sorted_points[i+1]]) <= epsilon:
            if square_dist(pivot, sorted_points[i]) > square_dist(pivot, sorted_points[i+1]):
                sorted_points.remove(sorted_points[i+1])
            else:
                sorted_points.remove(sorted_points[i])
        else:
            i += 1

    stack = [pivot, sorted_points[0], sorted_points[1]]

    i = 2
    while i < len(sorted_points):
        if det_3D_matrix(sorted_points[i],[stack[-2],stack[-1]]) < -epsilon:
            stack.pop()
        elif epsilon < det_3D_matrix(sorted_points[i],[stack[-2],stack[-1]]):
            stack.append(sorted_points[i])
            i += 1
        else:
            if square_dist(sorted_points[i], stack[-2]) > square_dist(stack[-1], stack[-2]):
                stack.pop()
                stack.append(sorted_points[i])
            i += 1

    return stack


def Jarvis(points, epsilon = 0):
    if len(points) < 3:
        raise ValueError("Graham Scan requires at least 3 points")

    points.sort( key=lambda p: (p[1], p[0]))
    stack = [points[0]]


    while True:
        next_point = None
        for p in points:
            if p == stack[-1]:
                continue
            if next_point is None or det_3D_matrix(p, [stack[-1], next_point]) < -epsilon:
                next_point = p
            elif epsilon > det_3D_matrix(p, [stack[-1], next_point]) > -epsilon:
                if square_dist(next_point, stack[-1]) < square_dist(p, stack[-1]):
                    next_point = p

        if next_point == points[0]:
            break
        stack.append(next_point)

    return stack


def scatter(points, name = None):
    setx = [x[0] for x in points]
    sety = [y[1] for y in points]
    plt.ylabel("Współrzędna Y")
    plt.xlabel("Współrzędna X")
    if name is not None:
        plt.title(f"Rys. {name}")

    plt.scatter(setx, sety)

def draw_lines(points):
    for i in range(len(points)):
        plt.plot([points[i][0],points[(i+1)%len(points)][0]],[points[i][1],points[(i+1)%len(points)][1]],
                 color= 'r')



set1 = generate_points(50000, [-100, 100], [-100, 100])
set2 = generate_circle_points(25000, 10)
set3 = generate_rectangle_points(25000, (-10, -10), (10, 10))
set4 = generate_square_points(6250, 6250, (0,0), 10)
graham_test_set = [(0,-5),(10,10),(0,50),(-10,10),(0,20), (-2,15),(2,15)]

'''Zbiory'''

# scatter(set1)
# plt.show()
#
# scatter(set2)
# plt.show()
#
# scatter(set3)
# plt.show()
#
# scatter(set4, "2.4")
# plt.show()

'''Otoczki zbiorów'''

# scatter(set1, "3.1 J")
# scatter(Jarvis(set1, 10 ** (-13)))
# draw_lines(Jarvis(set1, 10 ** (-13)))
# plt.show()
#
# scatter(set1, "3.1")
# scatter(Graham(set1, 10 ** (-13)))
# draw_lines(Graham(set1, 10 ** (-13)))
# plt.show()
#
#
# scatter(set2, "3.2 J")
# scatter(Jarvis(set2, 10 ** (-13)))
# draw_lines(Jarvis(set2, 10 ** (-13)))
# plt.show()
#
# scatter(set2, "3.2")
# scatter(Graham(set2, 10 ** (-13)))
# draw_lines(Graham(set2, 10 ** (-13)))
# plt.show()
#
#
# scatter(set3, "3.3 J")
# scatter(Jarvis(set3, 10 ** (-13)))
# draw_lines(Jarvis(set3, 10 ** (-13)))
# plt.show()
#
# scatter(set3, "3.3")
# scatter(Graham(set3, 10 ** (-13)))
# draw_lines(Graham(set3, 10 ** (-13)))
# plt.show()
#
#
# scatter(set4, "3.4 J")
# scatter(Jarvis(set4, 10**(-13)))
# draw_lines(Jarvis(set4, 10**(-13)))
# plt.show()
#
# scatter(set4, "3.4")
# scatter(Graham(set4, 10**(-13)))
# draw_lines(Graham(set4, 10**(-13)))
# plt.show()

'''Mierzenie czasu działania'''

used_set = set4

start_time = time.perf_counter()
Graham(used_set,10**(-13))
end_time = time.perf_counter()
print("Czas Grahama: " + str(end_time - start_time))

start_time = time.perf_counter()
Jarvis(used_set,10**(-13))
end_time = time.perf_counter()
print("Czas Jarvisa: " + str(end_time - start_time))

