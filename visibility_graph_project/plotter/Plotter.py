from math import inf

from Line import Line
from Point import Point
from VisibilityGraph import VisibilityGraph
from plotter.Plot import PlotSingle
from plotter.SequencePlotter import SequencePlotter


class Plotter:
    def __init__(self, draw_partial=False):
        self.xlim = [inf, -inf]
        self.ylim = [inf, -inf]
        self.draw_partial = draw_partial
        self.annotations = []

        self.partial_seqplot = None
        self.partial_plot_index = 0

        self.seqplot = SequencePlotter(f"visibility-sum-", "Kroki algorytmu")

    def init_limits(self, P):
        for i, p in enumerate(P):
            self.annotations.append(chr(ord("A")+i))
            self.xlim[0] = min(self.xlim[0], p.x)
            self.xlim[1] = max(self.xlim[1], p.x)
            self.ylim[0] = min(self.ylim[0], p.y)
            self.ylim[1] = max(self.ylim[1], p.y)

        # marginesy
        self.xlim[0] -= abs(self.xlim[0])*0.1
        self.xlim[1] += abs(self.xlim[1])*0.1
        self.ylim[0] -= abs(self.ylim[0])*0.1
        self.ylim[1] += abs(self.ylim[1])*0.1

    def new_partial_plot(self):
        self.partial_seqplot = SequencePlotter(f"visibility-step{self.partial_plot_index:03d}-", "Kroki algorytmu")
        self.partial_plot_index += 1

    def partial_plot(self, L, P, vg:VisibilityGraph, Sweeper):
        if not self.draw_partial:
            return

        plt:PlotSingle = self.partial_seqplot.next()
        plt.xlim(*self.xlim)
        plt.ylim(*self.ylim)

        # przeszkody
        plt.points_scatter(P, annotations=self.annotations)
        plt.lines_draw(L)

        # miotła
        plt.lines_draw([Line(Sweeper.p, Sweeper.w)], color="C3")
        plt.points_scatter([Sweeper.p], color="C1", zorder=40, s=24)

        plt.draw_and_save()

    def sum_up(self, L, P, vg:VisibilityGraph, Sweeper):
        plt:PlotSingle = self.seqplot.next()
        plt.xlim(*self.xlim)
        plt.ylim(*self.ylim)

        # przeszkody
        plt.points_scatter(P, s=16, color="C3", zorder=3, annotations=self.annotations)
        plt.lines_draw(L, linewidth=3, color="C3", zorder=2)

        # miotła (punkt)
        plt.points_scatter([Sweeper.p], color="C1", zorder=40, s=24)

        # graf
        for (u, v) in vg.get_lines():
            u = Point(u[0], u[1])
            v = Point(v[0], v[1])
            l = Line(u, v)
            plt.lines_draw([l], linewidth=1, zorder=3, color="k--")

        plt.draw_and_save()

