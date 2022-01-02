import math
from functools import cmp_to_key
from sortedcontainers import SortedList


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.figure = None
        self.visible = False
        self.line_to = []
        self.line_to_points_set = set()

    def with_line(self, point_line):
        self.line_to.append(point_line)
        self.line_to_points_set.add(point_line[0])
        return self

    def has_line_to(self, point):
        return point in self.line_to_points_set

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Line:
    def __init__(self, s, t):
        self.s = s
        self.t = t

    def __repr__(self):
        return f"[{self.s} -> {self.t}]"

    def __eq__(self, other):
        return self.s == other.s and self.t == other.t

    def __gt__(self, other):
        if self.s == other.t:
            if orient(Sweeper.p, self.s, self.t) > 0:
                if orient(self.t, self.s, other.s) < 0:
                    return True
                return False

            elif orient(Sweeper.p, self.s, self.t) < 0:
                if orient(self.t, self.s, other.s) > 0:
                    return True
                return False

            else:
                return dist(Sweeper.p, self.t) > dist(Sweeper.p, other.s)

        elif self.t == other.s:
            if orient(Sweeper.p, self.t, self.s) > 0:
                if orient(self.s, self.t, other.t) < 0:
                    return True
                return False

            elif orient(Sweeper.p, self.t, self.s) < 0:
                if orient(self.s, self.t, other.t) > 0:
                    return True
                return False

            else:
                return dist(Sweeper.p, self.s) > dist(Sweeper.p, other.t)

        return dist_p_to_intersection(Sweeper.p, Sweeper.w, self) > dist_p_to_intersection(Sweeper.p, Sweeper.w, other)


class Figure:
    def __init__(self, points=None):
        self.points = [] if points is None else points

    def __repr__(self):
        return f"<Figure points: {self.points}>"


class Sweeper:
    p = None
    w = None


class VisibilityGraph:
    def __init__(self, points):
        self.points = points
        self.graph = {x: {} for x in points}

    def add_edge(self, u, v):
        self.graph[u][v] = 1

    def get_points(self):
        return [(point.x, point.y) for point in self.points]

    def get_lines(self):
        lines = []
        for u, adjacent in self.graph.items():
            for v in adjacent.keys():
                lines.append([(u.x, u.y), (v.x, v.y)])

        return lines

    def get_lines_separately(self):
        all_lines = []
        for u, adjacent in self.graph.items():
            lines = []
            for v in adjacent.keys():
                lines.append([(u.x, u.y), (v.x, v.y)])
            all_lines.append(lines)

        return all_lines


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


def visibility_graph(figures):
    # utworzenie listy krawędzi oraz dodanie do wierzchołków informacji o incydentnych krawędziach
    L = []
    P = []
    for figure in figures:
        P += figure.points
        for i in range(len(figure.points)):
            u = figure.points[i - 1]
            v = figure.points[i]
            l = Line(u, v)
            u.with_line((v, l))
            v.with_line((u, l))
            v.figure = figure
            L.append(l)


    # stworzenie grafu widoczności
    vg = VisibilityGraph(P)

    for p in vg.points:
        # struktura zdarzeń
        Q1 = []
        Q2 = []
        for point in vg.points:
            if point == p:
                continue

            if point.y < p.y or (point.y == p.y and point.x > p.x):
                Q1.append(point)
            else:
                Q2.append(point)

        # sortowanie struktury zdarzeń
        Q1.sort(key=lambda a: dist(p, a))
        Q1.sort(key=cmp_to_key(lambda a, b: orient(p, a, b)))
        Q2.sort(key=lambda a: dist(p, a))
        Q2.sort(key=cmp_to_key(lambda a, b: orient(p, a, b)))
        Q = Q1 + Q2

        # struktura stanu
        T = SortedList()

        # dodanie do struktury stanu krawędzi przecinających miotłę w położeniu początkowym
        initial_sweep_line = Line(p, Point(10**20, p.y))
        Sweeper.p = p
        Sweeper.w = Point(10**20, p.y)
        for line in L:
            if orient(Sweeper.p, line.s, Sweeper.w) != 0 and orient(Sweeper.p, line.t, Sweeper.w) != 0 and intersection(line, initial_sweep_line):
                T.add(line)

        prev_w = None
        for i in range(len(Q)):
            w = Q[i]
            Sweeper.w = w

            if w.figure == p.figure:
                if w.has_line_to(p):
                    w.visible = True
                    vg.add_edge(p, w)

                else:
                    w.visible = False

            elif len(T) == 0:
                w.visible = True
                vg.add_edge(p, w)

            elif prev_w is None or orient(p, prev_w, w) != 0:
                if intersection(T[0], Line(p, w)):
                    w.visible = False

                else:
                    w.visible = True
                    vg.add_edge(p, w)

            elif not prev_w.visible:
                w.visible = False

            else:
                temp_point = Point(w.x, w.y)
                temp_line = Line(temp_point, temp_point)

                if intersection(T[T.bisect_left(temp_line) - 1], Line(p, w)):
                    w.visible = False

                else:
                    w.visible = True
                    vg.add_edge(p, w)


            for (u, l) in w.line_to:
                det_sign = orient(p, w, u)
                if det_sign < 0:
                    T.add(l)
                elif det_sign > 0 and l in T:
                    T.remove(l)

            prev_w = w

    # print(vg.graph)
    return vg
