import math
from random import uniform, randint, random
import matplotlib.pyplot as plt
import numpy as np


def linefrompoints(pointA, pointB):
    a = (pointA[1] - pointB[1]) / (pointA[0] - pointB[0])
    b = pointA[1] - a * pointA[0]

    return a, b

def det_2D_matrix(point, line):
    point = [point[0], point[1]]
    line[0] = [line[0][0], line[0][1]]
    line[1] = [line[1][0], line[1][1]]

    return (line[0][0] - point[0]) * (line[1][1] - point[1]) - (line[0][1] - point[1]) * (line[1][0] - point[0])
    # 0 - Na prostej
    # >0 - Nad prostą
    # <0 - Pod prostą

def det_3D_matrix(point, line):
    point = [point[0], point[1]]
    line[0] = [line[0][0], line[0][1]]
    line[1] = [line[1][0], line[1][1]]

    positive = (line[0][0] * line[1][1]) + (line[0][1] * point[0]) + (line[1][0] * point[1])
    negative = (line[1][1] * point[0]) + (line[0][0] * point[1]) + (line[0][1] * line[1][0])

    return positive - negative
    # 0 - Na prostej
    # >0 - Nad prostą
    # <0 - Pod prostą

def det_2D_numpy(point, line):
    px, py = point
    ax, ay = line[0]
    bx, by = line[1]

    arr = np.array([[ax - px, ay - py],[bx - px, by - py]])
    return np.linalg.det(arr)
    # 0 - Na prostej
    # >0 - Nad prostą
    # <0 - Pod prostą

def det_3D_numpy(point, line):
    px, py = point
    ax, ay = line[0]
    bx, by = line[1]

    arr = np.array([[ax,ay,1],[bx,by,1],[px,py,1]])
    return np.linalg.det(arr)

def generate_random_points(amount, rang):
    points = []

    for i in range(amount):
        points.append((uniform(rang[0], rang[1]), uniform(rang[0], rang[1])))

    return points

def generate_random_circle_points(amount, radius):
    points = []

    for i in range(amount):
        angle = uniform(0, 2 * math.pi)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        points.append((x, y))

    return points

def generate_random_line_points(amount, pointA, pointB, rang):
    points = []
    a, b = linefrompoints(pointA, pointB)

    for i in range(amount):
        x = uniform(rang[0], rang[1])
        points.append((x, a * x + b))

    return points

def show_set(set):
    setx = [x[0] for x in set]
    sety = [y[1] for y in set]

    plt.scatter(setx, sety, alpha=0.08)
    plt.ylabel("Współrzędna Y")
    plt.xlabel("Współrzędna X")
    plt.title("Rys. 2.4")
    plt.show()

def visualize(sett, line,det_func, name, acc = 0):
    abovex, abovey = [], []
    equalx, equaly = [], []
    belowx, belowy = [], []

    for point in sett:
        temp = det_func(point, line)
        if temp > acc:
            abovex.append(point[0])
            abovey.append(point[1])
        elif temp < -acc:
            belowx.append(point[0])
            belowy.append(point[1])
        else:
            equalx.append(point[0])
            equaly.append(point[1])


    plt.scatter(abovex,abovey, c='green', label="Nad")
    plt.scatter(equalx,equaly, c='red', label="Na")
    plt.scatter(belowx,belowy, c='blue', label="Pod")
    temp = "Rys. {name}".format(name=name)
    plt.title(temp)

    plt.legend(bbox_to_anchor=(0.355, 1.15), ncol=2)

    plt.show()

    # plt.bar(["Nad", "Na", "Pod"], [len(abovex), len(equalx), len(belowx)])
    # plt.title("Rys. 3.1")
    # plt.rcParams['font.size'] = '16'
    # plt.text(0, len(abovex), str(len(abovex)), ha='center')
    # plt.text(1, len(equalx), str(len(equalx)), ha='center')
    # plt.text(2, len(belowx), str(len(belowx)), ha='center')

    # print(len(abovex), len(equalx), len(belowx))
    # for i in range(len(equalx)):
    #     print(f'({equalx[i]},{equaly[i]})')
    # plt.show()


#/////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////////////////

set1 = generate_random_points(100000, [-1000,1000])
set2 = generate_random_points(100000, [-100000000000000, 100000000000000])
set3 = generate_random_circle_points(1000, 100)
set4 = generate_random_line_points(1000, (-1,0),(1,0.1), [-1000, 1000])

visualize(set1, [(-1,0), (1, 0.1)], det_2D_matrix,"3.1a", 0)
visualize(set3, [(-1,0), (1, 0.1)], det_2D_matrix, "3.2a", 0)

visualize(set4, [(-1,0), (1, 0.1)], det_2D_matrix, "3.3a", 0)
visualize(set4, [(-1,0), (1, 0.1)], det_3D_matrix, "3.4a", 0)
visualize(set4, [(-1,0), (1, 0.1)], det_2D_numpy, "3.5a", 0)
visualize(set4, [(-1,0), (1, 0.1)], det_3D_numpy, "3.6a", 0)

visualize(set2, [(-1,0), (1, 0.1)], det_2D_matrix, "3.7a", 0)