from helpers import dist

class VisibilityGraph:
    def __init__(self, points):
        self.points = points
        self.graph = {x: {} for x in points}

    def add_edge(self, u, v):
        self.graph[u][v] = dist(u, v)

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

    def get_graph(self):
        return self.graph

    def __repr__(self):
        return f"<Graph: {self.graph}>"
