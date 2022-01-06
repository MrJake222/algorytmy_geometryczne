from random import randint
from Point import Point
from Figure import Figure

# funkcja generuje n losowych kwadratów 1x1 na kwadratowej płaszczyźnie o boku długości side_len
def generate_random_figures(n, side_len):
    positions_taken = set()
    F = []

    while n > 0:
        x = 2 * randint(0, side_len // 2)
        y = 2 * randint(0, side_len // 2)
        if not (x, y) in positions_taken:
            positions_taken.add((x, y))
            F.append(Figure([Point(x, y), Point(x + 1, y), Point(x + 1, y + 1), Point(x, y + 1)]))
            n -= 1

    return F
