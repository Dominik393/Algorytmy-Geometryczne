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

    aviable_sides = [0, 1, 2, 3] # Dolna, Prawa, Górna, Lewa
    temp = random.randint(0, len(aviable_sides)-1)
    sides = [aviable_sides[temp]]
    aviable_sides.pop(temp)
    temp = random.randint(0, len(aviable_sides)-1)
    sides.append(aviable_sides[temp])

    for i in range(amount_per_side):
        for side in sides:
            if side == 0:
                x = random.uniform(lowerleft[0], lowerleft[0] + length)
                y = lowerleft[1]
                points.append((x,y))
            elif side == 1:
                x = lowerleft[0] + length
                y = random.uniform(lowerleft[1], lowerleft[1] + length)
                points.append((x,y))
            elif side == 2:
                x = random.uniform(lowerleft[0], lowerleft[0] + length)
                y = lowerleft[1] + length
                points.append((x, y))
            else:
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

        if next_point == points[0]:
            break
        stack.append(next_point)

    return stack


def visualize_prep(sett):
    setx = [x[0] for x in sett]
    sety = [y[1] for y in sett]

    plt.scatter(setx, sety)




set1 = generate_rectangle_points(200, (-10,-10),(10,10))
set2 = generate_circle_points(100, 10)
set3 = generate_points(100, [-100,100], [-100, 100])
set4 = generate_square_points(50, 50, (0,0), 10)


graham_test_set = [(0,-5),(10,10),(0,50),(-10,10),(0,20), (-2,15),(2,15)]

visualize_prep(set2)
plt.show()

start_time = time.perf_counter()
Jarvis(set2,10**(-13))
end_time = time.perf_counter()
print("Czas Jarvisa: " + str(end_time - start_time))

start_time = time.perf_counter()
Graham(set2,10**(-13))
end_time = time.perf_counter()
print("Czas Grahama: " + str(end_time - start_time))
