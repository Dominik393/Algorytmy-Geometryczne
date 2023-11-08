import math
import random
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


def Graham(sett):
    lowest_point = (float('inf'), float('inf'))
    to_skip = -1

    for i in range(0,len(sett)):
        if sett[i][1]  < lowest_point[1]:
            lowest_point = sett[i]
            to_skip = i
        elif sett[i][1] == lowest_point[1]:
            if sett[i][0] < lowest_point[0]:
                lowest_point = sett[i]
                to_skip = i

    negative_sett = []
    neutral_sett = []
    positive_sett = []

    for i in range(len(sett)):
        if i == to_skip:
            continue

        y_diff = lowest_point[1] - sett[i][1]
        x_diff = lowest_point[0] - sett[i][0]

        if x_diff == 0:
            neutral_sett.append([sett[i], float('inf')])
        elif (y_diff/x_diff) > 0:
            positive_sett.append([sett[i], (y_diff/x_diff)])
        else:
            negative_sett.append([sett[i], (y_diff/x_diff)])

    negative_sett.sort(key= lambda x: x[1])
    positive_sett.sort(key=lambda x: x[1])

    new_sett = positive_sett + neutral_sett + negative_sett
    del positive_sett, negative_sett, neutral_sett, x_diff, y_diff, to_skip
    new_sett = [x[0] for x in new_sett]

    print(len(new_sett))

    stack = [lowest_point, new_sett[0], new_sett[1]]

    i = 2
    while i < len(new_sett):
        if det_3D_matrix(new_sett[i], [stack[-1], stack[-2]]) > 1**(-14):
            stack.pop()
        elif det_3D_matrix(new_sett[i], [stack[-1], stack[-2]]) < -1**(-14):
            stack.append(new_sett[i])
            i+=1
        else:   # 2 ostatnie punkty są współniowe
            old_dist = ((stack[-1][0] - stack[-2][0])**2 + (stack[-1][1] - stack[-2][1])**2)**0.5
            new_dist = ((stack[i][0] - stack[-2][0]) ** 2 + (stack[i][1] - stack[-2][1]) ** 2) ** 0.5

            if new_dist > old_dist:
                stack.pop()
                stack.append(new_sett[i])

            i+=1

    visualize(stack)



def visualize(sett):
    setx = [x[0] for x in sett]
    sety = [y[1] for y in sett]

    plt.scatter(setx, sety)
    plt.show()




set1 = generate_rectangle_points(200, (-10,-10),(10,10))
set2 = generate_circle_points(200, 10)
set3 = generate_points(10, [-100,100], [-100, 100])
set4 = generate_square_points(50, 50, (0,0), 10)


graham_test_set = [(0,-5),(10,10),(0,50),(-10,10),(0,20), (-2,15),(2,15)]

visualize(set2)
Graham(set2)