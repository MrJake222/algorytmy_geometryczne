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
