from plotter.Plot import PlotSingle

class SequencePlotter:
    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.index = 1

    def next(self):
        plot = PlotSingle(f"out/{self.name}{self.index:03d}", size=(6, 6), dpi=300)
        plot.title(self.title)
        self.index += 1
        return plot