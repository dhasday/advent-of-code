import math

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day14Solver(DaySolver):
    year = 2024
    day = 14

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        size_x = 101
        size_y = 103
        mid_x = size_x // 2
        mid_y = size_y // 2

        robots = []
        for line in lines:
            values = helpers.parse_all_numbers(line)
            pos = values[0], values[1]
            vel = values[2], values[3]

            robots.append((pos, vel))

        ans_one = None
        min_safety_factor = math.inf
        min_time = None
        for i in range(10_000):
            quadrants = [0, 0, 0, 0]
            for pos, vel in robots:
                cur_pos = (pos[0] + (vel[0] * i)) % size_x, (pos[1] + (vel[1] * i)) % size_y
                if cur_pos[0] < mid_x:
                    if cur_pos[1] < mid_y:
                        quadrants[0] += 1
                    elif cur_pos[1] > mid_y:
                        quadrants[1] += 1
                elif cur_pos[0] > mid_x:
                    if cur_pos[1] < mid_y:
                        quadrants[2] += 1
                    elif cur_pos[1] > mid_y:
                        quadrants[3] += 1
            safety_factor = math.prod(quadrants)

            if safety_factor != 0 and safety_factor < min_safety_factor:
                min_safety_factor = safety_factor
                min_time = i

            if i == 100:
                ans_one = safety_factor

        return ans_one, min_time
