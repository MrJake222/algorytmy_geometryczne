from Sweeper import Sweeper
from helpers import orient, dist, dist_p_to_intersection


class Line:
    def __init__(self, s, t):
        self.s = s
        self.t = t

    def __repr__(self):
        return f"[{self.s} -> {self.t}]"

    def __eq__(self, other):
        return self.s == other.s and self.t == other.t

    def __gt__(self, other):
        if self.s == other.t:
            if orient(Sweeper.p, self.s, self.t) > 0:
                if orient(self.t, self.s, other.s) < 0:
                    return True
                return False

            elif orient(Sweeper.p, self.s, self.t) < 0:
                if orient(self.t, self.s, other.s) > 0:
                    return True
                return False

            else:
                return dist(Sweeper.p, self.t) > dist(Sweeper.p, other.s)

        elif self.t == other.s:
            if orient(Sweeper.p, self.t, self.s) > 0:
                if orient(self.s, self.t, other.t) < 0:
                    return True
                return False

            elif orient(Sweeper.p, self.t, self.s) < 0:
                if orient(self.s, self.t, other.t) > 0:
                    return True
                return False

            else:
                return dist(Sweeper.p, self.s) > dist(Sweeper.p, other.t)

        return dist_p_to_intersection(Sweeper.p, Sweeper.w, self) > dist_p_to_intersection(Sweeper.p, Sweeper.w, other)
