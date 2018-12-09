import re
from collections import defaultdict, deque

from common.day_solver import DaySolver

INPUT_REGEX = re.compile('')

NUM_PLAYERS = 470
NUM_MARBLES = 72170


class Day09Solver(DaySolver):
    year = 2018
    day = 9

    class Elf(object):
        def __init__(self, id):
            self.id = id
            self.points = 0

    def solve_puzzle_one(self):
        return self._play_game(NUM_PLAYERS, NUM_MARBLES)

    def solve_puzzle_two(self):
        return self._play_game(NUM_PLAYERS, NUM_MARBLES * 100)

    def _play_game(self, elves=9, num_marbles=25):
        points = [0] * elves
        circle = deque([0])

        for marble in range(1, num_marbles + 1):
            if marble % 23 == 0:
                circle.rotate(7)
                points[marble % elves] += marble + circle.pop()
                circle.rotate(-1)
            else:
                circle.rotate(-1)
                circle.append(marble)

        return max(points)
