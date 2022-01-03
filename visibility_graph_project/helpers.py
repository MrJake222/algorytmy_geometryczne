import math

def dist_p_to_intersection(p, w, line):
    a, b, c, d = line.s, line.t, p, w

    W = (b.x - a.x) * (c.y - d.y) - (b.y - a.y) * (c.x - d.x)
    Wt = (c.x - a.x) * (c.y - d.y) - (c.y - a.y) * (c.x - d.x)
    Wr = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    if W == 0:
        return (dist(p, line.s) + dist(p, line.t)) / 2

    t, r = Wt / W, Wr / W
    x, y = (c.x + r * (d.x - c.x), c.y + r * (d.y - c.y))

    return math.sqrt((x - p.x) ** 2 + (y - p.y) ** 2)


def intersection(line1, line2):
    a, b, c, d = line1.s, line1.t, line2.s, line2.t

    W = (b.x - a.x) * (c.y - d.y) - (b.y - a.y) * (c.x - d.x)
    Wt = (c.x - a.x) * (c.y - d.y) - (c.y - a.y) * (c.x - d.x)
    Wr = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    if W == 0:
        return False

    t, r = Wt/W, Wr/W

    # sprawdzenie czy przecięcie występuje na odcinkach
    if t >= 1 or t <= 0 or r >= 1 or r <= 0:
        return False

    return True


def orient(a, b, c):
    epsilon = 10 ** -9
    det = a.x * b.y + c.x * a.y + b.x * c.y - c.x * b.y - b.x * a.y - a.x * c.y

    if abs(det) < epsilon: return 0  # collinear
    if det > 0: return 1  # counter-clockwise
    return -1  # clockwise


def dist(a, b):
    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)