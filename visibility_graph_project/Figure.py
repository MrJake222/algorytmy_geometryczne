class Figure:
    def __init__(self, points=None):
        self.points = [] if points is None else points

    def __repr__(self):
        return f"<Figure points: {self.points}>"
