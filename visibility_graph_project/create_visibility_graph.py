from functools import cmp_to_key
from sortedcontainers import SortedList

from Point import Point
from Line import Line
from VisibilityGraph import VisibilityGraph
from Sweeper import Sweeper
from helpers import orient, dist, intersection


def create_visibility_graph(figures, plotter=None):
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

    if plotter != None: plotter.init_limits(P)

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

        if plotter != None: plotter.new_partial_plot()

        prev_w = None
        for i in range(len(Q)):
            w = Q[i]
            Sweeper.w = w

            if plotter != None: plotter.partial_plot(L, P, vg, Sweeper)

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

        if plotter != None: plotter.sum_up(L, P, vg, Sweeper)

    # print(vg.graph)
    return vg
