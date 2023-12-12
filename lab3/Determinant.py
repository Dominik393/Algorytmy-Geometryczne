def det_3D_matrix(a, b, c):
    positive = (a.val * b.y) + (a.y * c.val) + (b.val * c.y)
    negative = (b.y * c.val) + (a.val * c.y) + (a.y * b.val)

    return positive - negative
    # 0 - Na prostej
    # >0 - Nad prostą
    # <0 - Pod prostą