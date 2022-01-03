from Figure import Figure
from Point import Point
from create_visibility_graph import create_visibility_graph
from plotter.Plotter import Plotter

s = Point(0.1, 0.1)
t = Point(0.9, 0.9)

F = [Figure([Point(0.4653679653679653, 0.3225108225108225), Point(0.7099567099567099, 0.47510822510822515), Point(0.5735930735930735, 0.6774891774891776)])]
F += [Figure([s]), Figure([t])]

plotter = Plotter(draw_partial=True)

vg = create_visibility_graph(F, plotter)
print("finished")
