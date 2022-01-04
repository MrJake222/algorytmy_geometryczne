from functools import cmp_to_key
from sortedcontainers import SortedList

from Point import Point
from Line import Line
from VisibilityGraph import VisibilityGraph
from Sweeper import Sweeper
from helpers import orient, dist, intersection


from Figure import Figure



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

    # if plotter is not None: plotter.init_limits(P)

    # stworzenie grafu widoczności
    vg = VisibilityGraph(P)

    for p in vg.points[:1]:

        print("Punkt p: ", p)

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

        # if plotter is not None: plotter.new_partial_plot()

        print("Struktura stanu na początku:", T)

        prev_w = None
        for i in range(len(Q)):
            w = Q[i]
            Sweeper.w = w

            # if plotter is not None: plotter.partial_plot(L, P, vg, Sweeper)

            print("Przetwarzany punkt: ", w)


            if w.figure == p.figure:
                if w.has_line_to(p):
                    print("Widoczny 1")
                    w.visible = True
                    vg.add_edge(p, w)

                else:
                    print("Niewidoczny 2")
                    w.visible = False

            elif len(T) == 0:
                print("Widoczny 3")
                w.visible = True
                vg.add_edge(p, w)

            elif prev_w is None or orient(p, prev_w, w) != 0:
                if intersection(T[0], Line(p, w)):
                    print("Niewidoczny 4")
                    w.visible = False

                else:
                    print("Widoczny 5")
                    w.visible = True
                    vg.add_edge(p, w)

            elif not prev_w.visible:
                print("Niewidoczny 6")
                w.visible = False

            else:
                temp_point = Point(w.x, w.y)
                temp_line = Line(temp_point, temp_point)

                # TODO - jak są w tej samej figurze to trzeba jeszcze oddzielnie sprawdzić

                if intersection(T[T.bisect_left(temp_line) - 1], Line(p, w)):
                    print("Niewidoczny 7")
                    w.visible = False

                else:
                    print("Widoczny 8")
                    w.visible = True
                    vg.add_edge(p, w)


            for (u, l) in w.line_to:
                det_sign = orient(p, w, u)
                if det_sign < 0:
                    T.add(l)
                elif det_sign > 0 and l in T:
                    T.remove(l)

            prev_w = w
            print("Struktura stanu po przetworzeniu:", T)

        # if plotter is not None: plotter.sum_up(L, P, vg, Sweeper)

    # print(vg.graph)
    return vg

def main():
    # F = [Figure([Point(0.4, 0.6), Point(0.20129870129870128, 0.4004329004329005),
    #              Point(0.3971861471861472, 0.19480519480519484),
    #              Point(0.6125541125541125, 0.2597402597402598),
    #              Point(0.6, 0.4), Point(0.6074891774891775, 0.6101731601731602)])]

    F = [Figure([Point(0.45, 0.87), Point(0.17, 0.47), Point(0.49, 0.82)]),
         Figure([Point(0.6, 0.4), Point(0.42, 0.33), Point(0.54, 0.23)]),
         Figure([Point(0.8, 0.2), Point(0.85, 0.44), Point(0.96, 0.35)])]

    F = [Figure([Point(0.2, 0.8)])] + F

    create_visibility_graph(F)

if __name__ == '__main__':
    main()
