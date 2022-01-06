from functools import cmp_to_key
from sortedcontainers import SortedList

from Point import Point
from Line import Line
from VisibilityGraph import VisibilityGraph
from Sweeper import Sweeper
from helpers import orient, dist, intersection


def find_internal_lines(figure):
    n = len(figure.points)
    if n < 3:
        return

    for i in range(n):
        prev_u = figure.points[i]
        u = figure.points[(i + 1) % n]
        next_u = figure.points[(i + 2) % n]

        for j in range(3, n):
            v = figure.points[(i + j) % n]

            if orient(prev_u, u, next_u) > 0:
                if orient(prev_u, u, v) > 0 and orient(u, next_u, v) > 0:
                    u.internal_line_to_points_set.add(v)

            elif orient(prev_u, u, v) > 0 or orient(u, next_u, v) > 0:
                u.internal_line_to_points_set.add(v)


def create_visibility_graph(figures, plotter=None, limit=None):
    # utworzenie listy krawędzi, znalezienie krawędzi wewnętrznych figur oraz
    # dodanie do punktów informacji o incydentnych krawędziach i wielokącie do którego należą
    L = []
    P = []
    for figure in figures:
        find_internal_lines(figure)
        P += figure.points
        for i in range(len(figure.points)):
            u = figure.points[i - 1]
            v = figure.points[i]
            l = Line(u, v)
            u.with_line((v, l))
            v.with_line((u, l))
            v.figure = figure
            L.append(l)

    if plotter is not None: plotter.init_limits(P)

    # stworzenie grafu widoczności
    vg = VisibilityGraph(P)

    # do rysowania testów
    points = vg.points
    if limit != None: points = points[:limit]
        
    # rozpatrujemy kolejne punkty oznaczane jako p, wokół nich będziemy obracać miotłę
    for p in points:
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

        if plotter is not None: plotter.new_partial_plot()

        prev_w = None
        for i in range(len(Q)):
            # ustawiamy miotłę na kolejnym punkcie z struktury zdarzeń, oznaczamy ten punkt jako w
            w = Q[i]
            Sweeper.w = w

            if plotter is not None: plotter.partial_plot(L, P, vg, Sweeper)

            # jeśli p i w należą do tej samej figury i łącząca je linia przechodzi przez wnętrze figury, to punkt w nie jest widoczny
            if w.figure == p.figure and p.has_internal_line_to(w):
                w.visible = False

            # jeśli powyższy warunek nie jest spełniony i struktura stanu jest pusta to punkt w jest widoczny
            elif len(T) == 0:
                w.visible = True
                vg.add_edge(p, w)

            # jeśli powyższe warunki nie są spełnione i punkt w nie jest współliniowy z poprzednio rozważanym punktem,
            # to punkt w jest widoczny wtedy i tylko wtedy, gdy miotła nie przecina pierwszego odcinka z struktury stanu
            elif prev_w is None or orient(p, prev_w, w) != 0:
                if intersection(T[0], Line(p, w)):
                    w.visible = False
                else:
                    w.visible = True
                    vg.add_edge(p, w)

            # jeśli w jest współliniowy z poprzednio rozważanym punktem prev_w, ale prev_w nie był widoczny, to w też nie jest widoczny
            elif not prev_w.visible:
                w.visible = False

            # jeśli prev_w był widoczny, to musimy sprawdzić podobne warunki jak poprzednio, tylko zamiast  sprawdzać przecięcie
            # miotły z pierwszym odcinkiem z struktury stanu, to rozważamy odcinek znajdujący się pomiędzy prev_w i w
            else:
                temp_point = Point(w.x, w.y)
                temp_line = Line(temp_point, temp_point)

                if w.figure == prev_w.figure and prev_w.has_internal_line_to(w):
                    w.visible = False
                elif intersection(T[T.bisect_left(temp_line) - 1], Line(p, w)):
                    w.visible = False
                else:
                    w.visible = True
                    vg.add_edge(p, w)

            # dodajemy do struktury stanu odcinki leżące przed miotłą i usuwamy te leżąc za miotłą
            # odcinki wspóliniowe z miotłą pomijamy
            for (u, l) in w.line_to:
                det_sign = orient(p, w, u)
                if det_sign < 0:
                    T.add(l)
                elif det_sign > 0 and l in T:
                    T.remove(l)

            prev_w = w

        if plotter is not None: plotter.sum_up(L, P, vg, Sweeper)

    return vg
