from collections import defaultdict

from aoc.common.day_solver import DaySolver


class Day07Solver(DaySolver):
    year = 2025
    day = 7

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        start = lines[0].index('S')
        cur_beams = {start: 1}  # Beam pos: count
        num_splits = 0
        for line in lines[1:]:
            next_beams = defaultdict(int)
            for beam, count in cur_beams.items():
                if line[beam] == '^':
                    next_beams[beam - 1] += count
                    next_beams[beam + 1] += count
                    num_splits += 1
                else:
                    next_beams[beam] += count
            cur_beams = next_beams

        total_futures = sum(num for num in cur_beams.values())
        return num_splits, total_futures
