import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from Line import Line


def get_xlim_ylim(x, y):
    C = 1.1
    O = 0
    if min(*x, *y) == 0: O = 0.1 * max(*x, *y)
    return (min(x) * C - O, max(x) * C), (min(y) * C - O, max(y) * C)

class Scene:
    def __init__(self, name, rows=1, cols=1, size=(12, 12), dpi=100):
        self.name = name
        self.rows = rows
        self.cols = cols
        self.fig, self.axs = plt.subplots(nrows=rows, ncols=cols, figsize=(size[0]*cols, size[1]*rows), dpi=dpi, squeeze=False)

    def title(self, title, y=0.98):
        self.fig.suptitle(title, fontsize=24, fontweight="bold", y=y)

    def get_ax(self, row, col):
        return self.axs[row][col]

    def draw_and_save(self):
        # plt.grid(True)
        plt.savefig(f"{self.name}.jpg", bbox_inches="tight")
        plt.close(self.fig)

    def show(self):
        plt.show()
        plt.close(self.fig)


class Plot:
    def __init__(self, ax, equal_aspect=True):
        self.ax = ax
        if equal_aspect: self.ax.axes.set_aspect('equal')
        self.ax.axes.grid(True, which="both")
        self.ax.axes.set_axisbelow(True)

    def title(self, title):
        self.ax.title.set_text(title)

    def xlabel(self, label):
        self.ax.set_xlabel(label)

    def ylabel(self, label):
        self.ax.set_ylabel(label)

    def xlim(self, xmin, xmax):
        self.ax.set_xlim([xmin, xmax])

    def ylim(self, ymin, ymax):
        self.ax.set_ylim([ymin, ymax])

    def xscale(self, scale):
        self.ax.set_xscale(scale)

    def yscale(self, scale):
        self.ax.set_yscale(scale)

    def x_minor_ticks(self, ticks):
        self.ax.axes.set_xticks(ticks, minor=True)

    def x_Major_ticks(self, ticks):
        self.ax.axes.set_xticks(ticks, minor=False)

    def y_minor_ticks(self, ticks):
        self.ax.axes.set_yticks(ticks, minor=True)

    def y_Major_ticks(self, ticks):
        self.ax.axes.set_yticks(ticks, minor=False)

    def point(self, x, y, **kwargs):
        self.ax.plot([x], [y], **kwargs)
        return self

    def plot(self, *args, **kwargs):
        self.ax.plot(*args, **kwargs)
        return self

    def points_setup(self, P):
        x = [p.x for p in P]
        y = [p.y for p in P]
        xlim, ylim = get_xlim_ylim(x, y)

        self.xlabel("x")
        self.ylabel("y")
        self.xlim(*xlim)
        self.ylim(*ylim)
        self.ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        return self

    def points_scatter(self, points, s=10, zorder=0, color="C0", annotations=None):
        x = [p.x for p in points]
        y = [p.y for p in points]
        self.ax.scatter(x, y, color=color, s=s, zorder=zorder)

        if annotations != None:
            for i, p in enumerate(points):
                self.ax.annotate(annotations[i], (p.x, p.y), xytext=(0, 6),textcoords="offset points") # was (3,3)

    def lines_draw(self, lines, points=True, size=10, linewidth=1.5, zorder=1, color="C0"):
        for line in lines:
            s = line.s
            t = line.t
            if points:
                self.points_scatter((s, t), s=size, zorder=zorder+1)
            self.ax.plot((s.x, t.x), (s.y, t.y), color, linewidth=linewidth, zorder=zorder)

    def figures_draw(self, figures):
        points = []
        lines = []

        for f in figures:
            P = f.points
            for i in range(1, len(P)):
                u = P[i-1]
                v = P[i]
                points.append(u)
                lines.append(Line(u, v))
            lines.append(Line(P[-1], P[0]))
            points.append(P[-1])

        self.points_scatter(points)
        self.lines_draw(lines)

class PlotSingle(Plot):
    def __init__(self, name, size=(12, 12), dpi=100, equal_aspect=True):
        self.scene = Scene(name, size=size, dpi=dpi)
        super().__init__(self.scene.get_ax(0, 0), equal_aspect)

    def draw_and_save(self):
        self.scene.draw_and_save()

    def show(self):
        self.scene.show()