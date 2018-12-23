import re
from collections import defaultdict

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile('(-?\d+)')


class Day23Solver(DaySolver):
    year = 2018
    day = 23

    class Nanobot(object):
        def __init__(self, line):
            numbers = map(int, INPUT_REGEX.findall(line))
            self.pos = tuple(numbers[:-1])
            self.radius = numbers[-1]

        def __hash__(self):
            return hash(self.pos)

        def __cmp__(self, other):
            return cmp(self.pos, other.pos)

    def solve_puzzle_one(self):
        nanobots = self._load_input()

        ref_bot = sorted(nanobots, key=lambda n: -n.radius)[0]

        return len([b for b in nanobots if ref_bot.radius >= self._calculate_distance(b.pos, ref_bot.pos)])

    def solve_puzzle_two(self):
        """
        This is not a general solution, but works for my input since there are no large clusters of
        nanobots that don't overlap and skew that the counts.
        """
        nanobots = self._load_input()

        x_values = [b.pos[0] for b in nanobots]
        y_values = [b.pos[1] for b in nanobots]
        z_values = [b.pos[2] for b in nanobots]

        mins = [min(x_values), min(y_values), min(z_values)]
        maxs = [max(x_values), max(y_values), max(z_values)]

        max_size = max([maxs[0] - mins[0], maxs[1] - mins[1], maxs[2] - mins[2]]) + 1

        cur_step = 1
        while cur_step < max_size:
            cur_step *= 2

        max_dist = 0
        while cur_step:
            max_pos, max_dist = self._find_max_for_step(nanobots, cur_step, mins, maxs)

            mins = [p - cur_step for p in max_pos]
            maxs = [p + cur_step for p in max_pos]
            cur_step /= 2

        return max_dist

    def _find_max_for_step(self, nanobots, step, mins, maxs):
        max_count, max_pos, max_dist = 0, None, 0
        for x in xrange(mins[0], maxs[0], step):
            for y in xrange(mins[1], maxs[1], step):
                for z in xrange(mins[2], maxs[2], step):
                    cur_pos = (x, y, z)
                    cur_count = 0
                    for bot in nanobots:
                        distance = self._calculate_distance(bot.pos, cur_pos)
                        if (distance - bot.radius) / step <= 0:
                            cur_count += 1

                    if cur_count > max_count:
                        max_count = cur_count
                        max_pos = cur_pos
                        max_dist = self._calculate_distance(cur_pos, (0, 0, 0))
                    elif cur_count == max_count and cur_count > 0:
                        cur_dist = self._calculate_distance(cur_pos, (0, 0, 0))
                        if cur_dist < max_dist:
                            max_pos = cur_pos
                            max_dist = cur_dist
        return max_pos, max_dist

    def _load_input(self):
        return [self.Nanobot(l) for l in self._load_all_input_lines()]

    def _find_bot_with_largest_signal(self, nanobots):
        max_bot = nanobots[0]
        for bot in nanobots:
            if bot.radius > max_bot.radius:
                max_bot = bot
        return max_bot

    def _calculate_distance(self, pos_one, pos_two):
        return abs(pos_one[0] - pos_two[0]) \
                + abs(pos_one[1] - pos_two[1]) \
                + abs(pos_one[2] - pos_two[2])

    def _find_neighbors(self, nanobots):
        neighbors = defaultdict(lambda: [])

        for idx_one, bot_one in enumerate(nanobots):
            for bot_two in nanobots[idx_one + 1:]:
                distance = self._calculate_distance(bot_one.pos, bot_two.pos)
                if distance <= (bot_one.radius + bot_two.radius):
                    neighbors[bot_one].append(bot_two)
                    neighbors[bot_two].append(bot_one)

        return neighbors

