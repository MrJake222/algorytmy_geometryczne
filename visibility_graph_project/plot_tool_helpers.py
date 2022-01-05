from plot_tool import *
from create_visibility_graph import create_visibility_graph
from shortest_path import shortest_path
from Point import Point
from Figure import Figure


def visibility_graph_scenes(figures):
    vg = create_visibility_graph(figures)

    figures_lines_collections = [LinesCollection([[(figure.points[i - 1].x, figure.points[i - 1].y), (figure.points[i].x, figure.points[i].y)]
                                                  for i in range(len(figure.points))], color="tab:red", linestyle="dotted", zorder=2, linewidth=2.5) for figure in figures]

    points_collection = PointsCollection(vg.get_points(), color="tab:green", zorder=3, marker=".")
    lines_collection = LinesCollection(vg.get_lines(), color="tab:blue", zorder=1, linewidth=0.8)

    return [ Scene([points_collection], [lines_collection]) , Scene([points_collection], figures_lines_collections + [lines_collection]) ]


def visibility_graph_scenes_separately(figures):
    vg = create_visibility_graph(figures)

    figures_lines_collections = [LinesCollection([[(figure.points[i - 1].x, figure.points[i - 1].y), (figure.points[i].x, figure.points[i].y)]
                                                  for i in range(len(figure.points))], color="tab:red", linestyle="dotted", zorder=2, linewidth=2.5) for figure in figures]

    points_collection = PointsCollection(vg.get_points(), color="tab:green", zorder=3, marker=".")
    scenes = [Scene([points_collection], figures_lines_collections + [LinesCollection(lines, color="tab:blue", zorder=1, linewidth=1)]) for lines in vg.get_lines_separately()]

    return scenes


def shortest_path_scene(figures, s, t):
    d, path = shortest_path(figures, s, t)

    figures_lines_collections = [LinesCollection([[(figure.points[i - 1].x, figure.points[i - 1].y), (figure.points[i].x, figure.points[i].y)]
                                                  for i in range(len(figure.points))], color="tab:red", linestyle="dotted", zorder=2, linewidth=2.5) for figure in figures]
    points_collection = PointsCollection([(s.x, s.y), (t.x, t.y)], color="tab:green", zorder=3, marker=".")

    lines = []
    for i in range(1, len(path)):
        lines.append([(path[i - 1].x, path[i - 1].y), (path[i].x, path[i].y)])

    path_lines_collections = [LinesCollection(lines, color="tab:blue", zorder=1, linewidth=1)]

    return [ Scene([points_collection], figures_lines_collections + path_lines_collections) ]


def get_figures_from_plot(plot):
    figures = [Figure([Point(line[0][0], line[0][1]) for line in figure.lines]) for figure in plot.get_added_figure() if len(figure.lines) > 0]
    # zaokrąglenie do testów
    # figures = [Figure([Point(round(line[0][0], 2), round(line[0][1], 2)) for line in figure.lines]) for figure in plot.get_added_figure() if len(figure.lines) > 0]

    return figures


def get_points_from_plot(plot):
    return [Point(point[0], point[1]) for point in plot.get_added_points()[0].points]
