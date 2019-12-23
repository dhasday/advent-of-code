import math
import re
from collections import deque, defaultdict
from functools import reduce
from itertools import islice, cycle

from aoc.common.a_star_search import AStarSearch
from aoc.common.breadth_first_search import BreadthFirstSearch
from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.common.helpers import ALL_NUMBERS_REGEX, STANDARD_DIRECTIONS
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


class Day23Solver(DaySolver):
    year = 2019
    day = 23

    def solve_puzzle_one(self):
        # lines = self.load_all_input_lines()
        # line = self.load_only_input_line()
        return None

    def solve_puzzle_two(self):
        return None


if __name__ == '__main__':
    Day23Solver().print_results()
