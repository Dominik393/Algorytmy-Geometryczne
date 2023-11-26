def det_3D_matrix(a, b, c):
    positive = (a.x * b.y) + (a.y * c.x) + (b.x * c.y)
    negative = (b.y * c.x) + (a.x * c.y) + (a.y * b.x)

    return positive - negative
    # 0 - Na prostej
    # >0 - Nad prostą
    # <0 - Pod prostą