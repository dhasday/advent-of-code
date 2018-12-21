import re

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile('(\d+)x(\d+)x(\d+)')


class Day03Solver(DaySolver):
    year = 2015
    day = 3

    def solve_puzzle_one(self):
        return self._follow_orders(1)

    def solve_puzzle_two(self):
        return self._follow_orders(2)

    def _follow_orders(self, num_workers):
        orders = self._load_only_input_line()

        pos = [(0, 0) for _ in range(num_workers)]
        visited = set()
        visited.add(pos[0])

        for i in range(len(orders)):
            order = orders[i]

            if order == '>':
                change = 1, 0
            elif order == '<':
                change = -1, 0
            elif order == '^':
                change = 0, 1
            elif order == 'v':
                change = 0, -1
            else:
                change = 0, 0

            cur_worker = i % num_workers
            pos[cur_worker] = pos[cur_worker][0] + change[0], pos[cur_worker][1] + change[1]
            visited.add(pos[cur_worker])

        return len(visited)

